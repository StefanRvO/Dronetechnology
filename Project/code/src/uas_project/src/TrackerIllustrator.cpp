//This node subscribes on an image, a position and some offsets and overlays the positions and arrows onto the image.

#include <PID.hpp>
#include <ros/ros.h>
#include "std_msgs/Int16.h"
#include "geometry_msgs/Point.h"
#include <mutex>
#include <message_filters/time_synchronizer.h>
#include <message_filters/subscriber.h>
#include <message_filters/time_synchronizer.h>
#include <sensor_msgs/Image.h>
#include <sensor_msgs/CameraInfo.h>
#include <image_transport/image_transport.h>
#include "geometry_msgs/PointStamped.h"
#include "opencv2/opencv.hpp"
#include <cv_bridge/cv_bridge.h>


static image_transport::Publisher *overlay_pub = nullptr;

sensor_msgs::Image imageToMsg(cv::Mat &img)
{
    cv_bridge::CvImage img_bridge;
    sensor_msgs::Image img_msg;     // Message to be sent
    std_msgs::Header header; // empty header

    header.seq = 1; // user defined counter
    header.stamp = ros::Time::now(); // time

    img_bridge = cv_bridge::CvImage(header, sensor_msgs::image_encodings::BGR8, img); //RGB8 bgr8
    img_bridge.toImageMsg(img_msg); // from cv_bridge to sensor_msgs::Image

    return img_msg;
}


void all_callback(  const sensor_msgs::ImageConstPtr& camera_image,
                    const geometry_msgs::PointStamped::ConstPtr &pitch_offset,
                    const geometry_msgs::PointStamped::ConstPtr &roll_offset,
                    const geometry_msgs::PointStamped::ConstPtr &position)
{
    cv::Mat img = cv_bridge::toCvShare(camera_image, "bgr8")->image;
    cv::Point2f pos(position->point.x, position->point.y);
    cv::circle(img, pos, 10, cv::Scalar(0, 255, 0), 2);

    sensor_msgs::Image img_msg = imageToMsg(img);   // Convert webcam image to a ROS message


    overlay_pub->publish(img_msg);
}




int main(int argc, char **argv) {
    ros::init(argc, argv, "tracker_illustrator"); // Init ROS
    ros::NodeHandle nh; // Node handler
    image_transport::ImageTransport it(nh);
    overlay_pub = new image_transport::Publisher(it.advertise("/overlayed_image", 5) );   // Image publisher
    message_filters::Subscriber<sensor_msgs::Image> camera_sub(nh, "/camera_image", 5);

    message_filters::Subscriber<geometry_msgs::PointStamped> pitch_sub(nh, "/pitch_offset",5);
    message_filters::Subscriber<geometry_msgs::PointStamped> roll_sub(nh, "/roll_offset",5);
    message_filters::Subscriber<geometry_msgs::PointStamped> pos_subscriber(nh, "/ball_pos", 5);
    message_filters::TimeSynchronizer<sensor_msgs::Image, geometry_msgs::PointStamped, geometry_msgs::PointStamped, geometry_msgs::PointStamped> sync(camera_sub, pitch_sub, roll_sub, pos_subscriber, 10);
    sync.registerCallback(boost::bind(&all_callback, _1, _2, _3, _4));

    ros::spin();

    return 0;
}
