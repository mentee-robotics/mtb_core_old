cmake_minimum_required(VERSION 3.8)
project(state_publisher)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

add_executable(state_publisher_node src/state_publisher_node.cpp)
target_include_directories(state_publisher_node PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/description/")

install(
  DIRECTORY launch description configs
  DESTINATION share/${PROJECT_NAME}
)

install(TARGETS state_publisher_node
  DESTINATION lib/${PROJECT_NAME})

ament_package()
