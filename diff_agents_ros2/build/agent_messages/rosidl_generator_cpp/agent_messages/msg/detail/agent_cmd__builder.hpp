// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from agent_messages:msg/AgentCmd.idl
// generated code does not contain a copyright notice

#ifndef AGENT_MESSAGES__MSG__DETAIL__AGENT_CMD__BUILDER_HPP_
#define AGENT_MESSAGES__MSG__DETAIL__AGENT_CMD__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "agent_messages/msg/detail/agent_cmd__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace agent_messages
{

namespace msg
{

namespace builder
{

class Init_AgentCmd_agent_index
{
public:
  explicit Init_AgentCmd_agent_index(::agent_messages::msg::AgentCmd & msg)
  : msg_(msg)
  {}
  ::agent_messages::msg::AgentCmd agent_index(::agent_messages::msg::AgentCmd::_agent_index_type arg)
  {
    msg_.agent_index = std::move(arg);
    return std::move(msg_);
  }

private:
  ::agent_messages::msg::AgentCmd msg_;
};

class Init_AgentCmd_angular
{
public:
  explicit Init_AgentCmd_angular(::agent_messages::msg::AgentCmd & msg)
  : msg_(msg)
  {}
  Init_AgentCmd_agent_index angular(::agent_messages::msg::AgentCmd::_angular_type arg)
  {
    msg_.angular = std::move(arg);
    return Init_AgentCmd_agent_index(msg_);
  }

private:
  ::agent_messages::msg::AgentCmd msg_;
};

class Init_AgentCmd_linear
{
public:
  Init_AgentCmd_linear()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AgentCmd_angular linear(::agent_messages::msg::AgentCmd::_linear_type arg)
  {
    msg_.linear = std::move(arg);
    return Init_AgentCmd_angular(msg_);
  }

private:
  ::agent_messages::msg::AgentCmd msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::agent_messages::msg::AgentCmd>()
{
  return agent_messages::msg::builder::Init_AgentCmd_linear();
}

}  // namespace agent_messages

#endif  // AGENT_MESSAGES__MSG__DETAIL__AGENT_CMD__BUILDER_HPP_
