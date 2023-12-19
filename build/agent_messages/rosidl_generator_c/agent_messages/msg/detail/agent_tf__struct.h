// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from agent_messages:msg/AgentTF.idl
// generated code does not contain a copyright notice

#ifndef AGENT_MESSAGES__MSG__DETAIL__AGENT_TF__STRUCT_H_
#define AGENT_MESSAGES__MSG__DETAIL__AGENT_TF__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/AgentTF in the package agent_messages.
typedef struct agent_messages__msg__AgentTF
{
  double x;
  double y;
  double z;
  double roll;
  double pitch;
  double yaw;
  int32_t agent_index;
} agent_messages__msg__AgentTF;

// Struct for a sequence of agent_messages__msg__AgentTF.
typedef struct agent_messages__msg__AgentTF__Sequence
{
  agent_messages__msg__AgentTF * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} agent_messages__msg__AgentTF__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AGENT_MESSAGES__MSG__DETAIL__AGENT_TF__STRUCT_H_
