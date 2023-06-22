function toggleSidebar() {
  var sidebar = document.getElementById("sidebar");
  var content = document.getElementById("content");
  var sidebarToggle = document.getElementById("sidebar-toggle");

  sidebar.classList.toggle("sidebar-expanded");
  content.classList.toggle("content-moved");

  if (sidebar.classList.contains("sidebar-expanded")) {
    sidebarToggle.style.left = "160px";
  } else {
    sidebarToggle.style.left = "-40px";
  }
}
