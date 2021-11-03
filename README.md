# iris_model

Attempting to use amcl to localize robot in rviz.

### Begin mapping
```
roslaunch iris_model world.launch rviz:=true
rosrun iris_model teleop_twist_key.py 
roslaunch iris_model gmapping.launch 
rosrun map_server map_saver -f $(find iris_model)/maps/first_test_map
```
### Localize in map
```
roslaunch iris_model world.launch rviz:=true
rosrun iris_model teleop_twist_key.py 
roslaunch iris_model amcl.launch 
```
