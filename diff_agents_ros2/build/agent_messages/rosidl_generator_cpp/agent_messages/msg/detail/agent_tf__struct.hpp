// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from agent_messages:msg/AgentTF.idl
// generated code does not contain a copyright notice

#ifndef AGENT_MESSAGES__MSG__DETAIL__AGENT_TF__STRUCT_HPP_
#define AGENT_MESSAGES__MSG__DETAIL__AGENT_TF__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__agent_messages__msg__AgentTF __attribute__((deprecated))
#else
# define DEPRECATED__agent_messages__msg__AgentTF __declspec(deprecated)
#endif

namespace agent_messages
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct AgentTF_
{
  using Type = AgentTF_<ContainerAllocator>;

  explicit AgentTF_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0;
      this->y = 0.0;
      this->z = 0.0;
      this->roll = 0.0;
      this->pitch = 0.0;
      this->yaw = 0.0;
      this->agent_index = 0l;
    }
  }

  explicit AgentTF_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0;
      this->y = 0.0;
      this->z = 0.0;
      this->roll = 0.0;
      this->pitch = 0.0;
      this->yaw = 0.0;
      this->agent_index = 0l;
    }
  }

  // field types and members
  using _x_type =
    double;
  _x_type x;
  using _y_type =
    double;
  _y_type y;
  using _z_type =
    double;
  _z_type z;
  using _roll_type =
    double;
  _roll_type roll;
  using _pitch_type =
    double;
  _pitch_type pitch;
  using _yaw_type =
    double;
  _yaw_type yaw;
  using _agent_index_type =
    int32_t;
  _agent_index_type agent_index;

  // setters for named parameter idiom
  Type & set__x(
    const double & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const double & _arg)
  {
    this->y = _arg;
    return *this;
  }
  Type & set__z(
    const double & _arg)
  {
    this->z = _arg;
    return *this;
  }
  Type & set__roll(
    const double & _arg)
  {
    this->roll = _arg;
    return *this;
  }
  Type & set__pitch(
    const double & _arg)
  {
    this->pitch = _arg;
    return *this;
  }
  Type & set__yaw(
    const double & _arg)
  {
    this->yaw = _arg;
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
    agent_messages::msg::AgentTF_<ContainerAllocator> *;
  using ConstRawPtr =
    const agent_messages::msg::AgentTF_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<agent_messages::msg::AgentTF_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<agent_messages::msg::AgentTF_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      agent_messages::msg::AgentTF_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<agent_messages::msg::AgentTF_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      agent_messages::msg::AgentTF_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<agent_messages::msg::AgentTF_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<agent_messages::msg::AgentTF_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<agent_messages::msg::AgentTF_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__agent_messages__msg__AgentTF
    std::shared_ptr<agent_messages::msg::AgentTF_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__agent_messages__msg__AgentTF
    std::shared_ptr<agent_messages::msg::AgentTF_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const AgentTF_ & other) const
  {
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->z != other.z) {
      return false;
    }
    if (this->roll != other.roll) {
      return false;
    }
    if (this->pitch != other.pitch) {
      return false;
    }
    if (this->yaw != other.yaw) {
      return false;
    }
    if (this->agent_index != other.agent_index) {
      return false;
    }
    return true;
  }
  bool operator!=(const AgentTF_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct AgentTF_

// alias to use template instance with default allocator
using AgentTF =
  agent_messages::msg::AgentTF_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace agent_messages

#endif  // AGENT_MESSAGES__MSG__DETAIL__AGENT_TF__STRUCT_HPP_
