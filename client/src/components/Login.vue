<template>
  <b-container>
    <form class="form-signin" @submit.prevent="login">
      <h1 class="form-signin-heading">Please sign in</h1>
      <label for="inputEmail" class="sr-only">Email address</label>
      <input
        type="email"
        id="inputEmail"
        v-model="email"
        class="form-control"
        placeholder="Email address"
        required
        autofocus
      />
      <label for="inputPassword" class="sr-only">Password</label>
      <input
        type="password"
        id="inputPassword"
        v-model="password"
        class="form-control"
        placeholder="Password"
        required
      />
      <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
    </form>

    <div class="singin-with-group">
      <button class="btn btn-social-icon btn-github btn-indent" type="button" @click="github">
        <span><font-awesome-icon :icon="['fab', 'github']"/></span>
      </button>
      <button class="btn btn-social-icon btn-vk btn-indent" type="button" @click="vk">
        <span><font-awesome-icon :icon="['fab', 'vk']"/></span>
      </button>
      <button class="btn btn-social-icon btn-yandex btn-indent" type="button" @click="yandex">
        <span><font-awesome-icon :icon="['fab', 'yandex-international']"/></span>
      </button>
    </div>

    <b-alert class="form-signin-alert" v-if="showMessage" variant="warning" show
      >{{ message }}
    </b-alert>
  </b-container>
</template>

<script>
import axios from "axios";

export default {
  name: "Login",
  data() {
    return {
      email: "",
      password: "",
      message: "",
      showMessage: false,
      query: {
        token: this.$route.query.token,
        username: this.$route.query.username
      }
    };
  },
  watch: {
    // eslint-disable-next-line
    "$route.query"() {
      this.fetch();
    }
  },
  mounted() {
    if (this.$route.query.token) {
      this.fetch();
    }
  },
  methods: {
    login() {
      const { email } = this;
      const { password } = this;
      this.$store
        .dispatch("login", { email, password })
        .then(
          // eslint-disable-next-line
          res => {
            this.$router.push("/");
            // eslint-disable-next-line
            location.reload();
          },
          // eslint-disable-next-line
          error => {
            this.message = "Invalid credentials";
            this.showMessage = true;
          }
        )
        .catch(err => console.log(err));
    },
    github() {
      axios.get("http://localhost:5000/login/github/").then(resp => {
        // eslint-disable-next-line
        window.location = resp.data.link;
      });
    },
    vk() {
      axios.get("http://localhost:5000/login/vk/").then(resp => {
        // eslint-disable-next-line
        window.location = resp.data.link;
      });
    },
    yandex() {
      axios.get("http://localhost:5000/login/yandex/").then(resp => {
        // eslint-disable-next-line
        window.location = resp.data.link;
      });
    },
    fetch() {
      localStorage.setItem("token", this.query.token);
      localStorage.setItem("username", this.query.username);
      axios.defaults.headers.common.Authorization = this.query.token;
      this.$router.push("/");
      // eslint-disable-next-line
      location.reload();
    }
  }
};
</script>

<style scoped>
.form-signin {
  max-width: 330px;
  padding: 15px;
  margin: 0 auto;
}

.form-signin-alert {
  max-width: 300px;
  padding: 15px;
  margin: 30px auto 0;
}

.form-signin .form-signin-heading,
.form-signin {
  margin-bottom: 10px;
}

.form-signin {
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
