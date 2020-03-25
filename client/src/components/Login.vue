<template>
  <b-container>
    <navigation/>
    <form class="form-signin">
      <h1 class="form-signin-heading">Please sign in</h1>
      <label for="inputEmail" class="sr-only">Email address</label>
      <input type="email" id="inputEmail" class="form-control" placeholder="Email address" required
             autofocus>
      <label for="inputPassword" class="sr-only">Password</label>
      <input type="password" id="inputPassword" class="form-control" placeholder="Password"
             required>
      <div class="checkbox">
        <label>
          <input type="checkbox" value="remember-me"> Remember me
        </label>
      </div>
      <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
    </form>

    <div class="singin-with-group">
      <button class="btn btn-social-icon btn-github btn-indent" type="button">
        <span><font-awesome-icon :icon="['fab', 'github']"/></span>
      </button>
      <button class="btn btn-social-icon btn-vk btn-indent" type="button">
        <span><font-awesome-icon :icon="['fab', 'vk']"/></span>
      </button>
      <button class="btn btn-social-icon btn-yandex btn-indent" type="button">
        <span><font-awesome-icon :icon="['fab', 'yandex-international']"/></span>
      </button>
    </div>

  </b-container>
</template>

<script>
import Navigation from './Navigation.vue';

export default {
  name: 'Login',
  data() {
    return {
      input: {
        username: '',
        password: '',
      },
    };
  },
  components: {
    navigation: Navigation,
  },
  methods: {},
};
</script>

<style scoped>
  .form-signin {
    max-width: 330px;
    padding: 15px;
    margin: 0 auto;
  }

  .form-signin .form-signin-heading,
  .form-signin .checkbox {
    margin-bottom: 10px;
  }

  .form-signin .checkbox {
    font-weight: 400;
  }

  .form-signin .form-control {
    position: relative;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
    height: auto;
    padding: 10px;
    font-size: 16px;
  }

  .form-signin .form-control:focus {
    z-index: 2;
  }

  .form-signin input[type="email"] {
    margin-bottom: -1px;
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
  }

  .form-signin input[type="password"] {
    margin-bottom: 10px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
  }

  .singin-with-group {
    margin: auto;
    text-align: center;
  }

  .btn-indent {
    margin-left: 5px;
    margin-right: 5px;
  }
</style>
