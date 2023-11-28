// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from agent_messages:msg/AgentTF.idl
// generated code does not contain a copyright notice
#include "agent_messages/msg/detail/agent_tf__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
agent_messages__msg__AgentTF__init(agent_messages__msg__AgentTF * msg)
{
  if (!msg) {
    return false;
  }
  // x
  // y
  // z
  // roll
  // pitch
  // yaw
  // agent_index
  return true;
}

void
agent_messages__msg__AgentTF__fini(agent_messages__msg__AgentTF * msg)
{
  if (!msg) {
    return;
  }
  // x
  // y
  // z
  // roll
  // pitch
  // yaw
  // agent_index
}

bool
agent_messages__msg__AgentTF__are_equal(const agent_messages__msg__AgentTF * lhs, const agent_messages__msg__AgentTF * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // x
  if (lhs->x != rhs->x) {
    return false;
  }
  // y
  if (lhs->y != rhs->y) {
    return false;
  }
  // z
  if (lhs->z != rhs->z) {
    return false;
  }
  // roll
  if (lhs->roll != rhs->roll) {
    return false;
  }
  // pitch
  if (lhs->pitch != rhs->pitch) {
    return false;
  }
  // yaw
  if (lhs->yaw != rhs->yaw) {
    return false;
  }
  // agent_index
  if (lhs->agent_index != rhs->agent_index) {
    return false;
  }
  return true;
}

bool
agent_messages__msg__AgentTF__copy(
  const agent_messages__msg__AgentTF * input,
  agent_messages__msg__AgentTF * output)
{
  if (!input || !output) {
    return false;
  }
  // x
  output->x = input->x;
  // y
  output->y = input->y;
  // z
  output->z = input->z;
  // roll
  output->roll = input->roll;
  // pitch
  output->pitch = input->pitch;
  // yaw
  output->yaw = input->yaw;
  // agent_index
  output->agent_index = input->agent_index;
  return true;
}

agent_messages__msg__AgentTF *
agent_messages__msg__AgentTF__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  agent_messages__msg__AgentTF * msg = (agent_messages__msg__AgentTF *)allocator.allocate(sizeof(agent_messages__msg__AgentTF), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(agent_messages__msg__AgentTF));
  bool success = agent_messages__msg__AgentTF__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
agent_messages__msg__AgentTF__destroy(agent_messages__msg__AgentTF * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    agent_messages__msg__AgentTF__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
agent_messages__msg__AgentTF__Sequence__init(agent_messages__msg__AgentTF__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  agent_messages__msg__AgentTF * data = NULL;

  if (size) {
    data = (agent_messages__msg__AgentTF *)allocator.zero_allocate(size, sizeof(agent_messages__msg__AgentTF), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = agent_messages__msg__AgentTF__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        agent_messages__msg__AgentTF__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
agent_messages__msg__AgentTF__Sequence__fini(agent_messages__msg__AgentTF__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      agent_messages__msg__AgentTF__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

agent_messages__msg__AgentTF__Sequence *
agent_messages__msg__AgentTF__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  agent_messages__msg__AgentTF__Sequence * array = (agent_messages__msg__AgentTF__Sequence *)allocator.allocate(sizeof(agent_messages__msg__AgentTF__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = agent_messages__msg__AgentTF__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
agent_messages__msg__AgentTF__Sequence__destroy(agent_messages__msg__AgentTF__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    agent_messages__msg__AgentTF__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
agent_messages__msg__AgentTF__Sequence__are_equal(const agent_messages__msg__AgentTF__Sequence * lhs, const agent_messages__msg__AgentTF__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!agent_messages__msg__AgentTF__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
agent_messages__msg__AgentTF__Sequence__copy(
  const agent_messages__msg__AgentTF__Sequence * input,
  agent_messages__msg__AgentTF__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(agent_messages__msg__AgentTF);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    agent_messages__msg__AgentTF * data =
      (agent_messages__msg__AgentTF *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!agent_messages__msg__AgentTF__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          agent_messages__msg__AgentTF__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!agent_messages__msg__AgentTF__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
