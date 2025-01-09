#!/usr/bin/env bash
gnome-terminal --title "vlm_start" -x bash -c "cd ~/vlm_ws ; source install/setup.bash ; ros2 run live_llava vlm_start" &
gnome-terminal --title "vlm_pub" -- bash -c "cd ~/vlm_ws ; source install/setup.bash ; ros2 run live_llava vlm_pub" &
gnome-terminal --title "vlm_sub" -x bash -c "cd ~/vlm_ws ; source install/setup.bash ; ros2 run live_llava vlm_sub" &
