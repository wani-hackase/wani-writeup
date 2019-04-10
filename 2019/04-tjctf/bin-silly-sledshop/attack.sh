count=4286578688
while true
do
  echo python wu_solve003.py $count
  python solve_many.py $count
  count=`expr $count + 1000`
  if [ $count -gt  4294967295 ]; then
          exit 0
  fi
done
