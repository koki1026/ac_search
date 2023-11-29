// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from agent_messages:msg/AgentCmd.idl
// generated code does not contain a copyright notice

#ifndef AGENT_MESSAGES__MSG__DETAIL__AGENT_CMD__STRUCT_HPP_
#define AGENT_MESSAGES__MSG__DETAIL__AGENT_CMD__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'linear'
// Member 'angular'
#include "agent_messages/msg/detail/vector3__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__agent_messages__msg__AgentCmd __attribute__((deprecated))
#else
# define DEPRECATED__agent_messages__msg__AgentCmd __declspec(deprecated)
#endif

namespace agent_messages
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct AgentCmd_
{
  using Type = AgentCmd_<ContainerAllocator>;

  explicit AgentCmd_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : linear(_init),
    angular(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->agent_index = 0l;
    }
  }

  explicit AgentCmd_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : linear(_alloc, _init),
    angular(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->agent_index = 0l;
    }
  }

  // field types and members
  using _linear_type =
    agent_messages::msg::Vector3_<ContainerAllocator>;
  _linear_type linear;
  using _angular_type =
    agent_messages::msg::Vector3_<ContainerAllocator>;
  _angular_type angular;
  using _agent_index_type =
    int32_t;
  _agent_index_type agent_index;

  // setters for named parameter idiom
  Type & set__linear(
    const agent_messages::msg::Vector3_<ContainerAllocator> & _arg)
  {
    this->linear = _arg;
    return *this;
  }
  Type & set__angular(
    const agent_messages::msg::Vector3_<ContainerAllocator> & _arg)
  {
    this->angular = _arg;
    return *this;
  }
  Type & set__agent_index(
    const int32_t & _arg)
  {
    this->agent_index = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    agent_messages::msg::AgentCmd_<ContainerAllocator> *;
  using ConstRawPtr =
    const agent_messages::msg::AgentCmd_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<agent_messages::msg::AgentCmd_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<agent_messages::msg::AgentCmd_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      agent_messages::msg::AgentCmd_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<agent_messages::msg::AgentCmd_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      agent_messages::msg::AgentCmd_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<agent_messages::msg::AgentCmd_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<agent_messages::msg::AgentCmd_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<agent_messages::msg::AgentCmd_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__agent_messages__msg__AgentCmd
    std::shared_ptr<agent_messages::msg::AgentCmd_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__agent_messages__msg__AgentCmd
    std::shared_ptr<agent_messages::msg::AgentCmd_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const AgentCmd_ & other) const
  {
    if (this->linear != other.linear) {
      return false;
    }
    if (this->angular != other.angular) {
      return false;
    }
    if (this->agent_index != other.agent_index) {
      return false;
    }
    return true;
  }
  bool operator!=(const AgentCmd_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct AgentCmd_

// alias to use template instance with default allocator
using AgentCmd =
  agent_messages::msg::AgentCmd_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace agent_messages

#endif  // AGENT_MESSAGES__MSG__DETAIL__AGENT_CMD__STRUCT_HPP_
