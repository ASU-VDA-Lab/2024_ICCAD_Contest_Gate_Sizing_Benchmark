for dir in */; do
  cd "$dir" || exit
  bzip2 -d *
  cd ../
done

