if [[ "$(docker images -q avangard_ratings 2> /dev/null)" == "" ]]; then
  docker build -t avangard_ratings .
fi

docker run --rm -it -v ${PWD}/project:/project avangard_ratings

