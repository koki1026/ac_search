// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from agent_messages:msg/AgentCmd.idl
// generated code does not contain a copyright notice

#ifndef AGENT_MESSAGES__MSG__DETAIL__AGENT_CMD__TRAITS_HPP_
#define AGENT_MESSAGES__MSG__DETAIL__AGENT_CMD__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "agent_messages/msg/detail/agent_cmd__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'linear'
// Member 'angular'
#include "agent_messages/msg/detail/vector3__traits.hpp"

namespace agent_messages
{

namespace msg
{

inline void to_flow_style_yaml(
  const AgentCmd & msg,
  std::ostream & out)
{
  out << "{";
  // member: linear
  {
    out << "linear: ";
    to_flow_style_yaml(msg.linear, out);
    out << ", ";
  }

  // member: angular
  {
    out << "angular: ";
    to_flow_style_yaml(msg.angular, out);
    out << ", ";
  }

  // member: agent_index
  {
    out << "agent_index: ";
    rosidl_generator_traits::value_to_yaml(msg.agent_index, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const AgentCmd & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: linear
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "linear:\n";
    to_block_style_yaml(msg.linear, out, indentation + 2);
  }

  // member: angular
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "angular:\n";
    to_block_style_yaml(msg.angular, out, indentation + 2);
  }

  // member: agent_index
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "agent_index: ";
    rosidl_generator_traits::value_to_yaml(msg.agent_index, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const AgentCmd & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace agent_messages

namespace rosidl_generator_traits
{

[[deprecated("use agent_messages::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const agent_messages::msg::AgentCmd & msg,
  std::ostream & out, size_t indentation = 0)
{
  agent_messages::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use agent_messages::msg::to_yaml() instead")]]
inline std::string to_yaml(const agent_messages::msg::AgentCmd & msg)
{
  return agent_messages::msg::to_yaml(msg);
}

template<>
inline const char * data_type<agent_messages::msg::AgentCmd>()
{
  return "agent_messages::msg::AgentCmd";
}

template<>
inline const char * name<agent_messages::msg::AgentCmd>()
{
  return "agent_messages/msg/AgentCmd";
}

template<>
struct has_fixed_size<agent_messages::msg::AgentCmd>
  : std::integral_constant<bool, has_fixed_size<agent_messages::msg::Vector3>::value> {};

template<>
struct has_bounded_size<agent_messages::msg::AgentCmd>
  : std::integral_constant<bool, has_bounded_size<agent_messages::msg::Vector3>::value> {};

template<>
struct is_message<agent_messages::msg::AgentCmd>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AGENT_MESSAGES__MSG__DETAIL__AGENT_CMD__TRAITS_HPP_
