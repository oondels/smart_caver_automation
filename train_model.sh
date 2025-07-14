for i in $(seq 0 100); do
  printf "\rTraining Model: [%-50s] %3d%%" "$(printf '%0.s#' $(seq 1 $((i/2))))" "$i"
  sleep 2
done
echo
