//This node subscribes on an image, a position and some offsets and overlays the positions and arrows onto the image.

#include <PID.hpp>
#include <ros/ros.h>
#include "std_msgs/Int16.h"
#include "geometry_msgs/Point.h"
#include <mutex>


void imageCallback(const sensor_msgs::ImageConstPtr& msg)
{
}

void roll_callback(const geometry_msgs::PointStamped data)
{
}

void pitch_callback(const geometry_msgs::PointStamped data)
{
}

void pos_callback(geometry_msgs::PointStamped _point)
{
}

int main(int argc, char const **argv) {
    ros::init(argc, argv, "tracker_illustrator"); // Init ROS
    ros::NodeHandle nh; // Node handler
    image_transport::ImageTransport it(nh);
    image_transport::Subscriber camera_sub = it.subscribe("/camera_image", 5, imageCallback);   // Image receiver
    image_transport::Publisher overlay_pub = it.advertise("/overlayed_image", 5);   // Image publisher
    ros::Subscriber pitch_sub(nh->subscribe<geometry_msgs::PointStamped>("/pitch_offset",5, &pitch_callback, this)),
    ros::Subscriber roll_sub(nh->subscribe<geometry_msgs::PointStamped>("/roll_offset",5, &roll_callback, this))
    ros::Subscriber pos_subscriber = nh.subscribe<geometry_msgs::PointStamped>("/ball_pos", 1, pos_callback)),

    ros::spin();

    return 0;
}
