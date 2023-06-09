#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "mentee_messages/msg/motion_command.hpp"

using namespace std::chrono_literals;

/* This example creates a subclass of Node and uses std::bind() to register a
 * member function as a callback from the timer. */

class MtbControlPublisher : public rclcpp::Node
{
public:
  MtbControlPublisher()
  : Node("mtb_contorol_publisher"), count_(0)
  {
    publisher_ = this->create_publisher<mentee_messages::msg::MotionCommand>("my_cmd", 10);
    timer_ = this->create_wall_timer(
      500ms, std::bind(&MtbControlPublisher::timer_callback, this));
  }

private:
  void timer_callback()
  {
    auto str_message = std_msgs::msg::String();
    auto motion = mentee_messages::msg::MotionCommand();
    str_message.data = "Hello Menteebot! " + std::to_string(count_++);
    RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", str_message.data.c_str());
    //publisher_->publish(str_message);
    publisher_->publish(motion);

  }
  rclcpp::TimerBase::SharedPtr timer_;
  //rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::Publisher<mentee_messages::msg::MotionCommand>::SharedPtr publisher_;
  
  size_t count_;
};
int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MtbControlPublisher>());
  rclcpp::shutdown();
  return 0;
}
