import rospy 
from geometry_msgs.msg import PoseStamped, TransformStamped
from tf2_ros import TransformBroadcaster 

def tf_broadcaster():
    rospy.init_node("tf_broadcaster")
    rospy.Subscriber("/traj", PoseStamped, pose_cb)
    rospy.spin() 

def pose_cb(pose_msg):
    tf = TransformStamped()
    tf.header.stamp = pose_msg.header.stamp 
    tf.header.frame_id = pose_msg.header.frame_id
    tf.child_frame_id = "base_link"
    tf.transform.translation.x = pose_msg.pose.position.x
    tf.transform.translation.y = pose_msg.pose.position.y
    tf.transform.translation.z = pose_msg.pose.position.z 
    tf.transform.rotation.x = 0.0
    tf.transform.rotation.y = 0.0
    tf.transform.rotation.z = 0.0
    tf.transform.rotation.w = 1.0

    br.sendTransform(tf)

if __name__ == "__main__":
    br = TransformBroadcaster()
    try: 
        tf_broadcaster()
    except rospy.ROSInterruptException: 
        pass 