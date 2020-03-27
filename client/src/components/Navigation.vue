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
        <b-button-group v-if="!isLoggedIn">
          <router-link class="btn btn-outline-primary my-2 my-sm-0" to="/login">
            Sign in
          </router-link>
          <router-link class="btn btn-outline-primary my-2 my-sm-0" to="/register">
            Sign up
          </router-link>
        </b-button-group>
        <b-button-group v-if="isLoggedIn">
          <label class="d-inline p-2 bg-secondary text-white radius">Current user:
            {{ currentUser }}</label>
          <button type="button" class="btn btn-danger my-2 my-sm-0" @click="logout">
            Sign out
          </button>
        </b-button-group>
      </form>
    </div>
  </nav>
</template>

<script>
  export default {
    computed: {
      isLoggedIn: function () {
        return this.$store.getters.isLoggedIn
      },
      currentUser: function () {
        return this.$store.getters.userName
      },
    },
    methods: {
      logout: function () {
        this.$store.dispatch('logout')
          .then(() => {
            this.$router.push('/login')
          })
      }
    },
  }
</script>

<style scoped>
  .radius {
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
  }
</style>
