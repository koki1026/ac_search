// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from agent_messages:msg/AgentCmd.idl
// generated code does not contain a copyright notice

#ifndef AGENT_MESSAGES__MSG__DETAIL__AGENT_CMD__STRUCT_H_
#define AGENT_MESSAGES__MSG__DETAIL__AGENT_CMD__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'linear'
// Member 'angular'
#include "agent_messages/msg/detail/vector3__struct.h"

/// Struct defined in msg/AgentCmd in the package agent_messages.
typedef struct agent_messages__msg__AgentCmd
{
  agent_messages__msg__Vector3 linear;
  agent_messages__msg__Vector3 angular;
  int32_t agent_index;
} agent_messages__msg__AgentCmd;

// Struct for a sequence of agent_messages__msg__AgentCmd.
typedef struct agent_messages__msg__AgentCmd__Sequence
{
  agent_messages__msg__AgentCmd * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} agent_messages__msg__AgentCmd__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AGENT_MESSAGES__MSG__DETAIL__AGENT_CMD__STRUCT_H_
