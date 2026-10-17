#!/usr/bin/env bash
set -euo pipefail
cd "$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
source .local-apex/credentials.env
source scripts/apex-images.env
p() { podman --connection apex-cicd "$@"; }
# Keep matching static files in a named volume in the same VM.
p exec --user root apex-db bash -c 'cp -r /tmp/apex/images/. /opt/apex-images/ && chmod -R a+rX /opt/apex-images'
# Install as the normal image user, so wallet/config permissions match serving.
# Podman populates this new volume with the image directory's oracle ownership.
printf '%s\n%s\n' "$ORACLE_PASSWORD" "$ORDS_PASSWORD" |
  p run --rm -i --name apex-ords-install --network apex-net \
    -v apex-ords-config:/etc/ords/config:z \
    -v apex-images:/opt/oracle/apex/images:ro,z \
    "$ORDS_IMAGE" install --admin-user SYS --proxy-user \
    --db-hostname apex-db --db-port 1521 --db-servicename FREEPDB1 \
    --gateway-mode proxied --gateway-user APEX_PUBLIC_USER \
    --feature-sdw true --feature-rest-enabled-sql true --feature-db-api true \
    --password-stdin
for setting in 'standalone.static.path /opt/oracle/apex/images' \
               'plsql.gateway.mode proxied'; do
  # Intentional split: the two tokens are the property name and its value.
  p run --rm -v apex-ords-config:/etc/ords/config:z "$ORDS_IMAGE" config set $setting
done
p run -d --name apex-ords --network apex-net \
  -p 127.0.0.1:8080:8080 \
  -v apex-ords-config:/etc/ords/config:z \
  -v apex-images:/opt/oracle/apex/images:ro,z \
  --entrypoint /opt/graalvm-ee-java17/bin/java "$ORDS_IMAGE" \
  -jar /opt/oracle/ords/ords.war --config /etc/ords/config serve
