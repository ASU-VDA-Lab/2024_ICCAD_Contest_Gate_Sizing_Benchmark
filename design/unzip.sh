for dir in */; do
  cd "$dir" || exit
  bzip2 -z *
  cd ../
done

