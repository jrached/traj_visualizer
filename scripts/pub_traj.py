from numpy import load 

import rospy 
from geometry_msgs.msg import PoseStamped 

def get_trajs(file_path):
    data = load(file_path, allow_pickle=True)
    return data["acts"]

def pub_traj(trajs):
    pub = rospy.Publisher('/traj', PoseStamped, queue_size=10)
    rospy.init_node('traj_publisher')
    rate = rospy.Rate(10) # Publish at 10 Hz

    i = 0 
    dt = 3.0
    t0 = rospy.Time.now()
    while not rospy.is_shutdown():
        if trajs.shape[0] > i: 
            traj_point = trajs[:, 0, i]
            traj_pose = PoseStamped()
            traj_pose.header.stamp = rospy.Time.now()
            traj_pose.header.frame_id = "map"
            traj_pose.pose.position.x = traj_point[0]
            traj_pose.pose.position.y = traj_point[1]
            traj_pose.pose.position.z = traj_point[2] 
            
            print(traj_point)
            pub.publish(traj_pose)
            if (rospy.Time.now().secs + rospy.Time.now().nsecs / 1e9) - (t0.secs + t0.nsecs / 1e9) > dt: 
                t0 = rospy.Time.now()
                i += 1
            rate.sleep()
        else:
            rospy.loginfo("Trajectory Complete")

if __name__ == "__main__":
    file_path = '../data/panther/demos/round-000/dagger-demo-20230527_115723_444eec.npz'
    trajs = get_trajs(file_path)
    try: 
        pub_traj(trajs)
    except rospy.ROSInterruptException:
        pass 