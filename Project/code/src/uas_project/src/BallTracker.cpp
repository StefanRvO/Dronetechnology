#include "ros/ros.h"
#include "opencv2/opencv.hpp"
#include "std_msgs/String.h"
#include <sensor_msgs/Image.h>
#include <sensor_msgs/image_encodings.h>
#include <cv_bridge/cv_bridge.h>
#include <opencv2/highgui/highgui.hpp>
#include <cv_bridge/cv_bridge.h>
#include <image_transport/image_transport.h>
#include "geometry_msgs/PointStamped.h"
#include "HsvAdjust.hpp"

using namespace std;
using namespace cv;

static HsvAdjust adjust;
static ros::Publisher *ball_position_pub;


void imageCallback(const sensor_msgs::ImageConstPtr& msg)
{
  try
  {
  	Mat img = cv_bridge::toCvShare(msg, "bgr8")->image;  // Convert from ROS message to openCV image
    //adjust.guiSegmentation(img);  // Only for finding the correct settings for vison ball finding
    Point2f ballPosition = adjust.getBallPosition(img);

    geometry_msgs::PointStamped p;
    //std::cout << img.size() << std::endl;

    p.point.x = ballPosition.x - img.size().width / 2.;
    p.point.y = ballPosition.y - img.size().height / 2.;
    p.header.stamp = msg->header.stamp;
    ball_position_pub->publish(p);
  }
  catch (cv_bridge::Exception& e)
  {
    ROS_ERROR("Could not convert from '%s' to 'bgr8'.", msg->encoding.c_str());
  }
}


int main(int argc, char **argv)
{
    ros::init(argc, argv, "image_listener"); // Init ROS
    ros::NodeHandle nh; // Node handler
    ball_position_pub = new ros::Publisher(nh.advertise<geometry_msgs::PointStamped>("/ball_pos", 1));
    image_transport::ImageTransport it(nh);
    image_transport::Subscriber sub = it.subscribe("/camera_image", 5, imageCallback);   // Image receiver

    ros::spin();
    delete ball_position_pub;
}
