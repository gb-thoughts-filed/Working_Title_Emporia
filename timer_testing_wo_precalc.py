
from datetime import datetime
import time

counter = 0
title = datetime.today()
time_file = open(f"timer_testing_with_precalc{title: %B%d%Y}.txt", "a")
start_time = datetime.now()
t1 = time.time()

while time.time() - t1 < 3600:

    counter += 1

end_time = datetime.now()

time_file.write(f" \n {start_time}, {counter}, {end_time}")
