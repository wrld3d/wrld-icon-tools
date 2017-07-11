#!/bin/bash

# Assigns all tags from data/search_tags.json a coordinate, and then uploads
# them as points of interest to a WRLD points of interest set

# input is:
#   bash debug_icons_on_map.sh <DEVTOKEN>

# Trap errors #
error() {
  # Dump error location #
  local parent_lineno="$1"
  local message="$2"
  local code="${3:-1}"
  if [[ -n "$message" ]] ; then
    echo "Error on or near line ${parent_lineno}: ${message}; exiting with status ${code}"
  else
    echo "Error on or near line ${parent_lineno}; exiting with status ${code}"
  fi

  # Exit with original error code #
  exit "${code}"
}
trap 'error ${LINENO}' ERR

if [ ! -f ./data/search_tags.json ]; then
    echo "./data/search_tags.json does not exist"
    exit 0
fi

if [ -z "$(type -t jq)" ]; then
  echo "You are missing jq. Please install from https://stedolan.github.io/jq/"
  exit 1
fi

if [ "$#" -lt 1 ]; then
  echo "Devtoken required"
  exit 1
fi

if [ "$#" -gt 1 ]; then
  echo "Ensure only argument is a devtoken, and that there are no leading or
  trailing spaces"
  exit 1
fi

DEVTOKEN=$1
DATE=$(date)

SID=$(curl -s -XPOST https://poi.wrld3d.com/v1.1/poisets/?token=$DEVTOKEN -d \
"{\"name\":\"ICON TEST @ $DATE\"}" | jq '.id')

if [ "${#SID}" == 0 ]; then
    echo "Invalid devtoken provided. You may be using an API token instead of
    the devtoken"
    exit 1
fi

ZERO_LAT=56.4639943
ZERO_LON=-2.934169

INDEX=0
LENGTH=$(jq '.tags' ./data/search_tags.json | jq 'length')

if [ -z $LENGTH ]; then
  echo "./data/search_tags.json found, but unable to validate JSON"
  exit 1
fi

BULK_CREATE="{\"create\":["

while [ $INDEX -lt $LENGTH ]; do
  echo "Processing $(($INDEX + 1)) of $LENGTH"

  READABLE_TAG=$(jq '.tags' ./data/search_tags.json | jq ".[$INDEX] | .readable_tag")
  if [ "$READABLE_TAG" == "\"\"" ] || [ ${#READABLE_TAG} == 0 ]; then
    echo " - WARNING: readable_tag is missing"
    READABLE_TAG="\"readable_tag_missing\""
  fi

  TAGS=$(jq '.tags' ./data/search_tags.json | jq ".[$INDEX] | .tag")
  if [ "$TAGS" == "\"\"" ] || [ ${#TAGS} == 0 ]; then
    echo " - WARNING: tags are missing"
    TAGS="\"tags_are_missing\""
  fi

  COLUMN_WIDTH=20

  INDEX_DIVIDED_BY_COLUMN_WIDTH=$(($INDEX/$COLUMN_WIDTH))
  INDEX_MOD_COLUMN_WIDTH=$(($INDEX%$COLUMN_WIDTH))

  LAT=$(bc <<< "scale=3; $ZERO_LAT-($INDEX_DIVIDED_BY_COLUMN_WIDTH*(0.001))")
  LON=$(bc <<< "scale=3; $ZERO_LON+($INDEX_MOD_COLUMN_WIDTH*(0.001))")

  BULK_CREATE="$BULK_CREATE{
    \"title\":$READABLE_TAG,
    \"subtitle\":\"$(($INDEX + 1)) of $LENGTH\",
    \"tags\":$TAGS,
    \"lat\":$LAT,
    \"lon\":$LON
  }"

  ((INDEX++))

  if [ $INDEX -lt  $LENGTH ]; then
      BULK_CREATE="$BULK_CREATE,"
  fi
done

BULK_CREATE="$BULK_CREATE]}"

# echo
# echo "$BULK_CREATE"
# echo

echo
echo "...attempting to send post request o poi.wrld3d.com..."
echo
curl -v -XPOST https://poi.wrld3d.com/v1.1/poisets/$SID/bulk/?token=$DEVTOKEN -d "$BULK_CREATE"
echo
echo "...post request complete, see verbose message for details..."

echo
echo " 1] To interact with the WRLD POI API the SID for this
    set is: $SID see https://github.com/wrld3d/wrld-poi-api if you
    wish to use our API"
echo
echo " 2] You will need to refresh the map designer to see uploaded
    files"
echo
echo " 3] To view the places collection in your application, select
    the edit icon (a pencil) beside the Places Collection in the
    Places Designer, select \"+ Add An App\", then select the API
    key for the applications. You may need to generate and name an
    API key from the Developer Home:
    https://www.wrld3d.com/apikeys"

echo
echo "debug_icons_on_map.sh has finished"
echo
exit 0
