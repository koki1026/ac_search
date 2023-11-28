// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from agent_messages:msg/AgentTF.idl
// generated code does not contain a copyright notice

#ifndef AGENT_MESSAGES__MSG__DETAIL__AGENT_TF__BUILDER_HPP_
#define AGENT_MESSAGES__MSG__DETAIL__AGENT_TF__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "agent_messages/msg/detail/agent_tf__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace agent_messages
{

namespace msg
{

namespace builder
{

class Init_AgentTF_agent_index
{
public:
  explicit Init_AgentTF_agent_index(::agent_messages::msg::AgentTF & msg)
  : msg_(msg)
  {}
  ::agent_messages::msg::AgentTF agent_index(::agent_messages::msg::AgentTF::_agent_index_type arg)
  {
    msg_.agent_index = std::move(arg);
    return std::move(msg_);
  }

private:
  ::agent_messages::msg::AgentTF msg_;
};

class Init_AgentTF_yaw
{
public:
  explicit Init_AgentTF_yaw(::agent_messages::msg::AgentTF & msg)
  : msg_(msg)
  {}
  Init_AgentTF_agent_index yaw(::agent_messages::msg::AgentTF::_yaw_type arg)
  {
    msg_.yaw = std::move(arg);
    return Init_AgentTF_agent_index(msg_);
  }

private:
  ::agent_messages::msg::AgentTF msg_;
};

class Init_AgentTF_pitch
{
public:
  explicit Init_AgentTF_pitch(::agent_messages::msg::AgentTF & msg)
  : msg_(msg)
  {}
  Init_AgentTF_yaw pitch(::agent_messages::msg::AgentTF::_pitch_type arg)
  {
    msg_.pitch = std::move(arg);
    return Init_AgentTF_yaw(msg_);
  }

private:
  ::agent_messages::msg::AgentTF msg_;
};

class Init_AgentTF_roll
{
public:
  explicit Init_AgentTF_roll(::agent_messages::msg::AgentTF & msg)
  : msg_(msg)
  {}
  Init_AgentTF_pitch roll(::agent_messages::msg::AgentTF::_roll_type arg)
  {
    msg_.roll = std::move(arg);
    return Init_AgentTF_pitch(msg_);
  }

private:
  ::agent_messages::msg::AgentTF msg_;
};

class Init_AgentTF_z
{
public:
  explicit Init_AgentTF_z(::agent_messages::msg::AgentTF & msg)
  : msg_(msg)
  {}
  Init_AgentTF_roll z(::agent_messages::msg::AgentTF::_z_type arg)
  {
    msg_.z = std::move(arg);
    return Init_AgentTF_roll(msg_);
  }

private:
  ::agent_messages::msg::AgentTF msg_;
};

class Init_AgentTF_y
{
public:
  explicit Init_AgentTF_y(::agent_messages::msg::AgentTF & msg)
  : msg_(msg)
  {}
  Init_AgentTF_z y(::agent_messages::msg::AgentTF::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_AgentTF_z(msg_);
  }

private:
  ::agent_messages::msg::AgentTF msg_;
};

class Init_AgentTF_x
{
public:
  Init_AgentTF_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AgentTF_y x(::agent_messages::msg::AgentTF::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_AgentTF_y(msg_);
  }

private:
  ::agent_messages::msg::AgentTF msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::agent_messages::msg::AgentTF>()
{
  return agent_messages::msg::builder::Init_AgentTF_x();
}

}  // namespace agent_messages

#endif  // AGENT_MESSAGES__MSG__DETAIL__AGENT_TF__BUILDER_HPP_
