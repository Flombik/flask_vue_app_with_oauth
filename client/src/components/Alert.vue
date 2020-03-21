<template>
  <div>
    <b-alert variant="success" show> {{ message }} </b-alert>
    <br />
  </div>
</template>

<script>
export default {
  props: ["message"],
  data() {
    return {
      dismissSecs: 5,
      dismissCountDown: 0
    };
  },
  methods: {
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown;
    },
    showAlert() {
      this.dismissCountDown = this.dismissSecs;
    }
  }
};
</script>
