<template>
  <nav class="navbar fixed-top navbar-expand-md navbar-dark bg-dark mb-4">
    <div class="collapse navbar-collapse" id="navbarCollapse">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <router-link class="nav-link" to="/books">Books</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/authors">Authors</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/publishers">Publishers</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/genres">Genres</router-link>
        </li>
      </ul>
      <form class="form-inline mt-2 mt-md-0">
        <router-link class="btn btn-outline-primary my-2 my-sm-0" to="/login">Sign in</router-link>
      </form>
    </div>
  </nav>
</template>
