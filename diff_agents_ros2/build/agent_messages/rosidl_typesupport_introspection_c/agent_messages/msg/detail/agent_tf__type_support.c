// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from agent_messages:msg/AgentTF.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "agent_messages/msg/detail/agent_tf__rosidl_typesupport_introspection_c.h"
#include "agent_messages/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "agent_messages/msg/detail/agent_tf__functions.h"
#include "agent_messages/msg/detail/agent_tf__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void agent_messages__msg__AgentTF__rosidl_typesupport_introspection_c__AgentTF_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  agent_messages__msg__AgentTF__init(message_memory);
}

void agent_messages__msg__AgentTF__rosidl_typesupport_introspection_c__AgentTF_fini_function(void * message_memory)
{
  agent_messages__msg__AgentTF__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember agent_messages__msg__AgentTF__rosidl_typesupport_introspection_c__AgentTF_message_member_array[7] = {
  {
    "x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(agent_messages__msg__AgentTF, x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "y",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(agent_messages__msg__AgentTF, y),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "z",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(agent_messages__msg__AgentTF, z),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "roll",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(agent_messages__msg__AgentTF, roll),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "pitch",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(agent_messages__msg__AgentTF, pitch),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "yaw",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(agent_messages__msg__AgentTF, yaw),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "agent_index",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(agent_messages__msg__AgentTF, agent_index),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers agent_messages__msg__AgentTF__rosidl_typesupport_introspection_c__AgentTF_message_members = {
  "agent_messages__msg",  // message namespace
  "AgentTF",  // message name
  7,  // number of fields
  sizeof(agent_messages__msg__AgentTF),
  agent_messages__msg__AgentTF__rosidl_typesupport_introspection_c__AgentTF_message_member_array,  // message members
  agent_messages__msg__AgentTF__rosidl_typesupport_introspection_c__AgentTF_init_function,  // function to initialize message memory (memory has to be allocated)
  agent_messages__msg__AgentTF__rosidl_typesupport_introspection_c__AgentTF_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t agent_messages__msg__AgentTF__rosidl_typesupport_introspection_c__AgentTF_message_type_support_handle = {
  0,
  &agent_messages__msg__AgentTF__rosidl_typesupport_introspection_c__AgentTF_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_agent_messages
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, agent_messages, msg, AgentTF)() {
  if (!agent_messages__msg__AgentTF__rosidl_typesupport_introspection_c__AgentTF_message_type_support_handle.typesupport_identifier) {
    agent_messages__msg__AgentTF__rosidl_typesupport_introspection_c__AgentTF_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &agent_messages__msg__AgentTF__rosidl_typesupport_introspection_c__AgentTF_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
