// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from agent_messages:msg/AgentCmd.idl
// generated code does not contain a copyright notice
#include "agent_messages/msg/detail/agent_cmd__rosidl_typesupport_fastrtps_cpp.hpp"
#include "agent_messages/msg/detail/agent_cmd__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions
namespace agent_messages
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const agent_messages::msg::Vector3 &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  agent_messages::msg::Vector3 &);
size_t get_serialized_size(
  const agent_messages::msg::Vector3 &,
  size_t current_alignment);
size_t
max_serialized_size_Vector3(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace agent_messages

namespace agent_messages
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const agent_messages::msg::Vector3 &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  agent_messages::msg::Vector3 &);
size_t get_serialized_size(
  const agent_messages::msg::Vector3 &,
  size_t current_alignment);
size_t
max_serialized_size_Vector3(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace agent_messages


namespace agent_messages
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_agent_messages
cdr_serialize(
  const agent_messages::msg::AgentCmd & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: linear
  agent_messages::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.linear,
    cdr);
  // Member: angular
  agent_messages::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.angular,
    cdr);
  // Member: agent_index
  cdr << ros_message.agent_index;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_agent_messages
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  agent_messages::msg::AgentCmd & ros_message)
{
  // Member: linear
  agent_messages::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.linear);

  // Member: angular
  agent_messages::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.angular);

  // Member: agent_index
  cdr >> ros_message.agent_index;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_agent_messages
get_serialized_size(
  const agent_messages::msg::AgentCmd & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: linear

  current_alignment +=
    agent_messages::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.linear, current_alignment);
  // Member: angular

  current_alignment +=
    agent_messages::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.angular, current_alignment);
  // Member: agent_index
  {
    size_t item_size = sizeof(ros_message.agent_index);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_agent_messages
max_serialized_size_AgentCmd(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;


  // Member: linear
  {
    size_t array_size = 1;


    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      current_alignment +=
        agent_messages::msg::typesupport_fastrtps_cpp::max_serialized_size_Vector3(
        inner_full_bounded, inner_is_plain, current_alignment);
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: angular
  {
    size_t array_size = 1;


    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      current_alignment +=
        agent_messages::msg::typesupport_fastrtps_cpp::max_serialized_size_Vector3(
        inner_full_bounded, inner_is_plain, current_alignment);
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: agent_index
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  return current_alignment - initial_alignment;
}

static bool _AgentCmd__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const agent_messages::msg::AgentCmd *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _AgentCmd__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<agent_messages::msg::AgentCmd *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _AgentCmd__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const agent_messages::msg::AgentCmd *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _AgentCmd__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_AgentCmd(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _AgentCmd__callbacks = {
  "agent_messages::msg",
  "AgentCmd",
  _AgentCmd__cdr_serialize,
  _AgentCmd__cdr_deserialize,
  _AgentCmd__get_serialized_size,
  _AgentCmd__max_serialized_size
};

static rosidl_message_type_support_t _AgentCmd__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_AgentCmd__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace agent_messages

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_agent_messages
const rosidl_message_type_support_t *
get_message_type_support_handle<agent_messages::msg::AgentCmd>()
{
  return &agent_messages::msg::typesupport_fastrtps_cpp::_AgentCmd__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, agent_messages, msg, AgentCmd)() {
  return &agent_messages::msg::typesupport_fastrtps_cpp::_AgentCmd__handle;
}

#ifdef __cplusplus
}
#endif
