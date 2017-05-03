#!/bin/bash
version_number=$1
version_label=v$version_number

s3_bucket=$2
output_path=./output
dest_url_root=$s3_bucket/$version_label

cf_invalidation=$3
cf_invalidation_path=$4

function perform_s3_copy() {
  source_path=$1
  destination_url=$2
  recursive=$3

  aws s3 cp $source_path $destination_url $recursive --acl public-read
  if [ $? -ne 0 ] ; then  
    echo "Failed to upload site" >&2
    echo "If unable to locate credentials, set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables" >&2
    exit 1
  fi  
}

function upload_assets() {
  platform_suffix=$1
  echo "Uploading $platform_suffix assets..."
  perform_s3_copy $output_path/$platform_suffix $dest_url_root/assets/$platform_suffix --recursive
}

platforms=(ios android windows js)

for platform in "${platforms[@]}"
do
  upload_assets $platform
done

echo "Uploading tags..."
perform_s3_copy ./data/search_tags.json $dest_url_root/tags/search_tags.json

echo "Copying to latest..."
perform_s3_copy $dest_url_root $s3_bucket/latest --recursive

echo "Issuing CloudFront invalidation..."
aws configure set preview.cloudfront true
aws cloudfront create-invalidation --distribution-id cf_invalidation --paths cf_invalidation_path