---
name: digital-signature
description: Seal a file or a forensic hash-manifest with a legally-recognized digital signature plus an RFC-3161 timestamp — provable identity + provable time over exact bytes. Multiple PEER signer paths, chosen by legal level and availability: a government smart-card cert via PKCS#11 (qualified/QES), a recognized commercial QTSP S/MIME X.509 cert via gpgsm (advanced/AdES, no card needed), and an OpenPGP hardware token as an independent anchor — composed as two-pass sealing (sign now with what is recognized and available, countersign to qualified later over the same bytes). Invoke to sign evidence manifests, captured-image hash lists, git trees, or any artefact that must be attributable and time-anchored.
roles: [security]
---

# Digital signature (recognized cert + RFC-3161 timestamp)

Goal: bind **who** (a recognized signing cert) and **when** (TSA timestamp) to the **exact bytes**
(sha256) of the evidence manifest. Run on the clean host. The card is *one* signer path (§card);
when it is unavailable or you only need an advanced signature, use a peer path (§peers) — the card
being absent is an alternative, not a failure.

## The signer — SignMc (Monaco eID), how to use
The concrete implementation of this skill's card+PIN signing is **SignMc** (`~/src/SafeKeepIt/SignMc`):
the operator's **Monaco (Monco) eID** — a Gemalto/Thales IAS-ECC "MROAD" card driven by a **patched
OpenSC** in an isolated prefix (`opensc-local/`, the system OpenSC is untouched) + **pyHanko** for PAdES.
- **PKCS#11 module:** `opensc-local/lib/opensc-pkcs11.so` — use this everywhere below, not the system
  `/usr/lib/opensc-pkcs11.so`.
- **Signing cert:** `MROAD IAS Certificate 2` (Non-Repudiation, key ref **0x82**) — the document one;
  public cert at `my-signing-cert.pem`. (Auth cert `0x81` is NOT for signing.)
- **Sign a PDF / manifest-as-PDF:** FIRST close every other app that touches the card (Firefox,
  Thunderbird, Chromium, LibreOffice — `pkill -x soffice.bin`); the card is single-app and the lock
  bites at PIN time. Then `./sign-pdf-direct.py` (reads the cert on a non-auth session first, so
  contention aborts BEFORE the PIN and never wastes a retry) and enter the Code PIN once.
  Timestamp: `TSA_URL=http://timestamp.digicert.com ./sign-pdf-direct.py`.
- ⚠ **PIN retries are limited** — a few wrong PINs block the card (unblock with PUK). Ask the PIN ONCE.
- Full install is reversible: `./uninstall-monco.sh`.

For the CMS/manifest route below, substitute `P11=opensc-local/lib/opensc-pkcs11.so` and the 0x82 cert.

## Peer signer paths (§peers) — pick by legal level + availability, and compose them
The seal binds who + when + exact bytes; several *recognized* signer paths do that. Choose by the
**legal level** you need and what is available — and compose them: **two independent signatures over
one hash** is the ETSI crypto-agility posture (one trust-model/algorithm can be retired without
losing assurance). This is not a card-vs-fallback split; they are peers.

**Path A — gov smart-card (§card above).** Monaco eID via PKCS#11 → **qualified (QES)**, the
handwritten-equivalent level. Needs the card + PIN.

**Path B — commercial QTSP S/MIME X.509, via gpgsm (no card).** e.g. Certum/Asseco — an **EUTL-listed
QTSP**, **Individual-Validated** (the CA verified the natural person), key usage
`digitalSignature nonRepudiation`. A genuine EU-recognized identity binding — but a *software* key
with no QSCD, so it is **advanced (AdES), not qualified**. It is NOT a self-run CA (§legal): it carries
real signature identity, just not the qualified *level*.
```bash
FPR=0x<full-sha1-fingerprint>      # PIN the FINGERPRINT, never the email (two certs per email → wrong one signs)
gpgsm -u "$FPR" --detach-sign --armor -o "$MAN.p7s" "$MAN"     # detached CMS / CAdES-BES
gpgsm --verify "$MAN.p7s" "$MAN"                               # MUST print "Good signature" + a valid chain
```
gpgsm reaches this cert directly (stock scdaemon can't drive a patched-OpenSC gov card — that is
Path A's job). Confirm the chain shows `[certificate is good]` up to a trusted root.

**Path C — OpenPGP hardware anchor (Nitrokey).**
`gpg -u <keyid> --detach-sign --armor -o "$MAN.asc" "$MAN"`. Hardware-held, independent trust model.
OpenPGP is **not** an eIDAS AdES format, so it *corroborates* (a second independent who+when anchor) —
never the legal primary on its own.

**Two-pass sealing (the composition).** Seal NOW with whatever is recognized-and-available (Path B is
fine when the level is disclosed) + the timestamp; **upgrade to QES later** by countersigning the SAME
bytes with the qualified cert (Path A) when the card is in hand. The first-pass seal is never replaced —
the early time anchor is preserved. Qualified is an added layer, not a prerequisite.

**Git trees** use this same cert path applied to commits: `git config gpg.format x509;
git config user.signingkey <FPR>` (gpgsm is git's x509 backend — pin the fingerprint). Per-commit sigs
carry **no** timestamp, so anchor time by timestamping a seal over the whole tree bundle, not per commit.

## 1. Build the manifest to sign
List every artefact and its hash — never sign the big images directly, sign the manifest of hashes:
```bash
CASE=neptune; MAN=/home/sudoku/rescue/coc/${CASE}.manifest.txt
{
  echo "# $CASE evidence manifest"; echo "operator: S. Lambla"; echo "host: $(hostname)";
  echo "built-utc: $(date -u +%FT%TZ)"; echo;
  # one line per file: sha256  size  path  (add serials/S3 version-ids as available)
  find /path/to/images -type f -print0 | xargs -0 sha256sum
} > "$MAN"
sha256sum "$MAN"                     # the digest we actually sign
```

## 2. Find the smart-card signing key (PKCS#11)
```bash
P11=/usr/lib/opensc-pkcs11.so                 # or the card vendor's module
pkcs11-tool --module "$P11" -O                # list objects; note the signing cert/key label+id
pkcs15-tool --list-certificates               # confirm the gov cert is present
```

## 3. Sign the manifest (CMS / PKCS#7 detached, via the card)
```bash
# export the signer cert once (public):
pkcs11-tool --module "$P11" -r --type cert --id <ID> -o signer.crt.der
openssl x509 -inform der -in signer.crt.der -out signer.crt.pem
# detached CMS signature over the manifest, key stays on the card:
openssl cms -sign -binary -in "$MAN" \
  -signer signer.crt.pem \
  -keyform engine -engine pkcs11 -inkey "pkcs11:object=<label>;type=private" \
  -outform DER -out "$MAN.p7s" -nodetach:false 2>/dev/null || \
  echo "if openssl-pkcs11 engine is unavailable, sign via the card's own tool or the PDF route (§5)"
```

## 4. Add an RFC-3161 timestamp over the signature (provable time)
Same TSA you use for PAdES PDF signing. Timestamp the **signature file** (or the manifest digest):
```bash
TSA_URL="https://<your-tsa>"                 # the qualified TSA from your PDF workflow
openssl ts -query -data "$MAN.p7s" -sha256 -cert -out "$MAN.tsq"
curl -s -H "Content-Type: application/timestamp-query" \
     --data-binary @"$MAN.tsq" "$TSA_URL" -o "$MAN.tsr"
openssl ts -reply -in "$MAN.tsr" -text | head          # inspect: genTime = the anchored time
```

## 5. Pragmatic alternative — reuse the PDF/PAdES pipeline you already trust
If the CMS+engine path is fiddly, wrap the manifest text into a PDF and sign it with the **exact
cert + TSA flow you use for documents** (PAdES-LTV). The guarantee is identical: gov cert + qualified
timestamp over the content. Keep the source `.manifest.txt` alongside the signed PDF.

## 6. Verify + record
```bash
openssl cms -verify -in "$MAN.p7s" -inform DER -content "$MAN" -CAfile <gov-ca-chain>.pem
openssl ts -verify -data "$MAN.p7s" -in "$MAN.tsr" -CAfile <tsa-ca-chain>.pem
```
Log the signature (signer cert subject/serial, manifest sha256, TSA genTime) into the chain-of-custody
record (see `chain-of-custody`). Store `MAN`, `MAN.p7s`, `MAN.tsr` (or the signed PDF) **together**,
and — for cloud — under Object Lock (see `write-to-s3`).

## ⚠ What a signature does and does NOT do — READ before relying on it for law enforcement
A signature + qualified timestamp proves **integrity from the moment you sealed it** and **who**
sealed it — nothing more. It does **NOT** establish that what you extracted is a **faithful,
complete, reproducible acquisition of the source.** So "mount, copy the files out, sign them" is
**not** a forensically-sound acquisition on its own — it's a signed *copy of your analysis*.

For evidence going to police, meet **ISO/IEC 27037** (identification → collection → acquisition →
preservation; principles: **auditability, repeatability, reproducibility**):
- **Acquire the source properly** = a *verified forensic image*, defined concretely as:
  (1) source behind a **write-blocker** (hardware > software — disclose which);
  (2) a **complete bit-stream image of the whole physical device** — every sector, incl.
      unallocated/slack/HPA/DCO — NOT the logical filesystem;
  (3) a standard format — **E01/EWF** (self-documenting: embeds hashes + case metadata + integrity
      CRCs) or raw `dd`/AFF4;
  (4) **SHA-256 computed DURING acquisition**, then a **verification pass** where source-hash =
      image-hash = re-read-hash (a three-way match proves the copy is bit-exact);
  (5) a **validated tool** (NIST-CFTT / SWGDE-tested — `ewfacquire`/guymager/FTK Imager/dc3dd),
      recording tool+version, operator, timestamps, source serial, and write-blocker used.
  Analyse the image, never the original. (Encrypted source: the image captures **ciphertext**,
  verified by its hash; the decrypt+extract is a *separately documented, reproducible* analysis step
  run on the image — same recovery key + tool params → same plaintext files → same file hashes.)
- **Reproducibility is what convinces a court, not your signature:** document the exact process
  (image → hash → decrypt with recovery key X → `apfs-fuse -o xid=Y` → extract → hash) so an
  independent examiner re-runs it and gets the **same files and same hashes**.
- **Cleanest path for police:** preserve the **physical drive** write-blocked + sealed with the
  custody log and let the **police's certified lab do the acquisition**. Your own work then stands as
  a documented **investigative lead** (what's there, the decrypt method, your hashes) — explicitly
  labelled *owner's own read-only, non-certified analysis*, exactly as `EVIDENCE-HANDLING-LOG.md`
  already frames it. Do not overstate a software-write-blocked FUSE read as a certified acquisition.
- **Use the cert your JURISDICTION legally recognizes — never a self-run CA.** The seal's legal weight
  comes from a cert recognized for *signature value* where the case is heard:
  **Monaco (recipient here = Monaco police): the owner's government smart-card cert is treated as
  eIDAS-EQUIVALENT under Monaco's aligned framework — use it as the qualified seal.** EU = eIDAS
  Qualified (timestamp Art 42 presumes time + integrity; signature Art 25 = handwritten); US = FRE
  901 / 902(14). A **self-run CA** (the owner's `seb.house` CA / `pki-piv` intermediaries) is only an
  *advanced* signature — internal integrity only, **NO legal signature value** — never the legal seal.
  Add an **RFC-3161 timestamp** regardless (proves *when*).
  ⚠ **The signature's qualified status is not universally court-recognized** — so the PRIMARY
  evidentiary weight must come from the **ISO-27037 acquisition + hash reproducibility** (which stands
  on its own in any court); the Monaco-card signature *corroborates* who+when, it is not the sole
  foundation. The seal makes the manifest admissible; it does not substitute for a sound acquisition.
- **Format ≠ legal level — never conflate them.** **PAdES / CAdES / XAdES are signature *formats*** —
  they prove *who* signed and that the content is intact. ***Qualified* (eIDAS / Monaco-recognized) is a
  legal *level*** — the right to sign any legal act, handwritten-equivalent. A PAdES signature is
  *qualified* ONLY when made with a **qualified certificate**; the format alone does NOT confer it. Here
  the **Monaco government cert** supplies the qualified legal capacity and **PAdES** is just the wrapper —
  so write "qualified electronic signature, applied in PAdES format," never "PAdES = qualified/eIDAS."

## Gotchas (each has bitten this work)
- **Sign the plaintext manifest, never a ciphertext.** Encrypted blobs (gpg output, OpenTofu
  AES-GCM state) re-nonce on every write, so a signature over ciphertext never re-verifies. Sign the
  plaintext/canonical form; store the ciphertext separately.
- **A signature with no timestamp dies at cert expiry.** Per-artefact / per-commit sigs carry no
  time; the RFC-3161 token (§4) is what keeps them verifiable after the signing cert lapses (LTV).
  Timestamp every seal — especially short-lived commercial certs (~1 yr).
- **gpgsm `relax` in the trustlist loosens chain checks** — cross-verify with stock `openssl cms
  -verify` so the record is "checkable by anyone with ordinary tools" (ETSI Annex G), not dependent
  on your local trust config.

## Rules
- Sign the **manifest of hashes**, not the multi-TB images (the hashes bind the images).
- The private key never leaves the card. Card present only during signing.
- The TSA proves when the manifest was **signed** — timestamp right after each capture so sign-time
  tracks capture-time; log capture-time separately.
- **Hardware-token interaction (operator gate):** before ANY command that needs the operator to
  touch / insert / re-seat / pull the card or token, print a CAPS-UPPERCASE warning and DO NOT run it
  until the operator says "y". Ask for a PIN/password only ONCE — retries are limited (a few wrong PINs
  block the card; unblock with PUK). All cert/key material (keys, CSRs, `.cer`/`.p12`, backups) targets
  `~/certs`.
