// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from agent_messages:msg/AgentCmd.idl
// generated code does not contain a copyright notice

#ifndef AGENT_MESSAGES__MSG__DETAIL__AGENT_CMD__FUNCTIONS_H_
#define AGENT_MESSAGES__MSG__DETAIL__AGENT_CMD__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "agent_messages/msg/rosidl_generator_c__visibility_control.h"

#include "agent_messages/msg/detail/agent_cmd__struct.h"

/// Initialize msg/AgentCmd message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * agent_messages__msg__AgentCmd
 * )) before or use
 * agent_messages__msg__AgentCmd__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_agent_messages
bool
agent_messages__msg__AgentCmd__init(agent_messages__msg__AgentCmd * msg);

/// Finalize msg/AgentCmd message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_agent_messages
void
agent_messages__msg__AgentCmd__fini(agent_messages__msg__AgentCmd * msg);

/// Create msg/AgentCmd message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * agent_messages__msg__AgentCmd__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_agent_messages
agent_messages__msg__AgentCmd *
agent_messages__msg__AgentCmd__create();

/// Destroy msg/AgentCmd message.
/**
 * It calls
 * agent_messages__msg__AgentCmd__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_agent_messages
void
agent_messages__msg__AgentCmd__destroy(agent_messages__msg__AgentCmd * msg);

/// Check for msg/AgentCmd message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_agent_messages
bool
agent_messages__msg__AgentCmd__are_equal(const agent_messages__msg__AgentCmd * lhs, const agent_messages__msg__AgentCmd * rhs);

/// Copy a msg/AgentCmd message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_agent_messages
bool
agent_messages__msg__AgentCmd__copy(
  const agent_messages__msg__AgentCmd * input,
  agent_messages__msg__AgentCmd * output);

/// Initialize array of msg/AgentCmd messages.
/**
 * It allocates the memory for the number of elements and calls
 * agent_messages__msg__AgentCmd__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_agent_messages
bool
agent_messages__msg__AgentCmd__Sequence__init(agent_messages__msg__AgentCmd__Sequence * array, size_t size);

/// Finalize array of msg/AgentCmd messages.
/**
 * It calls
 * agent_messages__msg__AgentCmd__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_agent_messages
void
agent_messages__msg__AgentCmd__Sequence__fini(agent_messages__msg__AgentCmd__Sequence * array);

/// Create array of msg/AgentCmd messages.
/**
 * It allocates the memory for the array and calls
 * agent_messages__msg__AgentCmd__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_agent_messages
agent_messages__msg__AgentCmd__Sequence *
agent_messages__msg__AgentCmd__Sequence__create(size_t size);

/// Destroy array of msg/AgentCmd messages.
/**
 * It calls
 * agent_messages__msg__AgentCmd__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_agent_messages
void
agent_messages__msg__AgentCmd__Sequence__destroy(agent_messages__msg__AgentCmd__Sequence * array);

/// Check for msg/AgentCmd message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_agent_messages
bool
agent_messages__msg__AgentCmd__Sequence__are_equal(const agent_messages__msg__AgentCmd__Sequence * lhs, const agent_messages__msg__AgentCmd__Sequence * rhs);

/// Copy an array of msg/AgentCmd messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_agent_messages
bool
agent_messages__msg__AgentCmd__Sequence__copy(
  const agent_messages__msg__AgentCmd__Sequence * input,
  agent_messages__msg__AgentCmd__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // AGENT_MESSAGES__MSG__DETAIL__AGENT_CMD__FUNCTIONS_H_
