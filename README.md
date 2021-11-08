# iris_model

Attempting to use amcl to localize robot in rviz.

### Begin mapping
```
roslaunch iris_model bringup_iris_gmapping.launch
rosrun iris_model teleop_twist_key.py 
```
### Localize in map
```
roslaunch iris_model bringup_iris_amcl.launch
```
