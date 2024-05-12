for dir in */; do
  if [[ "$dir" == "util/" ]]; then
    continue
  fi
  cd "$dir" || exit
  bzip2 -d *
  cd ../
done

