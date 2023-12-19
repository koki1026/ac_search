// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from agent_messages:msg/AgentTF.idl
// generated code does not contain a copyright notice

#ifndef AGENT_MESSAGES__MSG__DETAIL__AGENT_TF__TRAITS_HPP_
#define AGENT_MESSAGES__MSG__DETAIL__AGENT_TF__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "agent_messages/msg/detail/agent_tf__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace agent_messages
{

namespace msg
{

inline void to_flow_style_yaml(
  const AgentTF & msg,
  std::ostream & out)
{
  out << "{";
  // member: x
  {
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << ", ";
  }

  // member: y
  {
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << ", ";
  }

  // member: z
  {
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
    out << ", ";
  }

  // member: roll
  {
    out << "roll: ";
    rosidl_generator_traits::value_to_yaml(msg.roll, out);
    out << ", ";
  }

  // member: pitch
  {
    out << "pitch: ";
    rosidl_generator_traits::value_to_yaml(msg.pitch, out);
    out << ", ";
  }

  // member: yaw
  {
    out << "yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.yaw, out);
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
  const AgentTF & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << "\n";
  }

  // member: y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << "\n";
  }

  // member: z
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
    out << "\n";
  }

  // member: roll
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "roll: ";
    rosidl_generator_traits::value_to_yaml(msg.roll, out);
    out << "\n";
  }

  // member: pitch
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pitch: ";
    rosidl_generator_traits::value_to_yaml(msg.pitch, out);
    out << "\n";
  }

  // member: yaw
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.yaw, out);
    out << "\n";
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

inline std::string to_yaml(const AgentTF & msg, bool use_flow_style = false)
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
  const agent_messages::msg::AgentTF & msg,
  std::ostream & out, size_t indentation = 0)
{
  agent_messages::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use agent_messages::msg::to_yaml() instead")]]
inline std::string to_yaml(const agent_messages::msg::AgentTF & msg)
{
  return agent_messages::msg::to_yaml(msg);
}

template<>
inline const char * data_type<agent_messages::msg::AgentTF>()
{
  return "agent_messages::msg::AgentTF";
}

template<>
inline const char * name<agent_messages::msg::AgentTF>()
{
  return "agent_messages/msg/AgentTF";
}

template<>
struct has_fixed_size<agent_messages::msg::AgentTF>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<agent_messages::msg::AgentTF>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<agent_messages::msg::AgentTF>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AGENT_MESSAGES__MSG__DETAIL__AGENT_TF__TRAITS_HPP_
