<template>
  <b-container>
    <form class="form-signup" @submit.prevent="register">
      <h1 class="form-signup-heading">Please sign up</h1>
      <label for="inputEmail" class="sr-only">Email address</label>
      <input type="email" id="inputEmail" v-model="email" class="form-control"
             placeholder="Email address" required
             autofocus>
      <label for="inputPassword" class="sr-only">Password</label>
      <input type="password" id="inputPassword" v-model="password" class="form-control"
             placeholder="Password"
             required>
      <label for="confirmPassword" class="sr-only">Confirm password</label>
      <input type="password" id="confirmPassword" v-model="password_confirmation"
             class="form-control" placeholder="Confirm password"
             required>
      <button class="btn btn-lg btn-primary btn-block" type="submit">Sign up</button>
      <alert class="alert-mr" :message="message" v-if="showMessage"/>
    </form>

  </b-container>
</template>

<script>
  import Alert from "./Alert";

  export default {
    data() {
      return {
        email: "",
        password: "",
        password_confirmation: "",
        message: "",
        showMessage: false,
      }
    },
    components: {
      alert: Alert,
    },
    methods: {
      register: function () {
        let data = {
          email: this.email,
          password: this.password,
        };
        this.$store.dispatch('register', data)
          .then((res) => {
            this.message = res.data.message;
            this.showMessage = true;
            this.email = "";
            this.password = "";
            this.password_confirmation = "";
          })
          .catch(err => console.log(err))
      }
    },
  }
</script>

<style scoped>
  .alert-mr {
    margin-top: 30px;
  }

  .form-signup {
    max-width: 330px;
    padding: 15px;
    margin: 0 auto;
  }

  .form-signup .form-signup-heading,
  .form-signup {
    margin-bottom: 10px;
  }

  .form-signup {
    font-weight: 400;
  }

  .form-signup .form-control {
    position: relative;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
    height: auto;
    padding: 10px;
    font-size: 16px;
  }

  .form-signup .form-control:focus {
    z-index: 2;
  }

  .form-signup input[id="inputEmail"] {
    margin-bottom: -1px;
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
  }

  .form-signup input[id="inputPassword"] {
    border-radius: 0;
  }

  .form-signup input[id="confirmPassword"] {
    margin-top: -1px;
    margin-bottom: 10px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
  }
</style>
