#!/bin/bash
SCRIPT_NAMES="
jquery.ui.widget.js
jquery.iframe-transport.js
jquery.fileupload.js
invisibleroads-uploads.js
"
pushd node_modules/invisibleroads-uploads > /dev/null
cat $SCRIPT_NAMES > main.js
popd > /dev/null
refresh-assets \
    invisibleroads_posts \
    invisibleroads_uploads
