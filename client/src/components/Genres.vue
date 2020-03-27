<template>
  <b-container>
    <div class="comp-style">
      <div class="table-width">
        <h1>Genres</h1>
        <br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success" v-if="isLoggedIn" v-b-modal.genre-modal>
          Add Genre
        </button>
        <br><br>
        <table class="table table-hover">
          <thead class="thead-light">
          <tr>
            <th scope="col">Genre</th>
            <th v-if="isLoggedIn"/>
          </tr>
          </thead>
          <tbody v-for="(genre, index) in genres" :key="index">
          <tr>
            <td>{{ genre.genre }}</td>
            <td class="btn-gr-ud" v-if="isLoggedIn">
              <button
                type="button"
                class="btn btn-danger btn-sm"
                @click="onDeleteGenre(genre)">
                Delete
              </button>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addGenreModal"
             id="genre-modal"
             title="Add a new genre"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-genre-group"
                      label="Genre:"
                      label-for="form-genre-input">
          <b-form-input id="form-genre-input"
                        type="text"
                        v-model="addGenreForm.genre"
                        required
                        placeholder="Enter genre">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </b-container>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      genres: [],
      addGenreForm: {
        genre: '',
      },
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  computed: {
      isLoggedIn: function () {
        return this.$store.getters.isLoggedIn
      }
    },
  methods: {
    getGenres() {
      const path = 'http://localhost:5000/genres/';
      axios.get(path)
        .then((res) => {
          this.genres = res.data.genres;
        })
        .catch((error) => {
          // eslint-отключение следующей строки
          console.error(error);
        });
    },
    addGenre(payload) {
      const path = 'http://localhost:5000/genres/add/';
      axios.post(path, payload)
        .then((res) => {
          this.getGenres();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-отключение следующей строки
          console.log(error);
          this.getGenres();
        });
    },
    initForm() {
      this.addGenreForm.genre = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addGenreModal.hide();
      const payload = {
        genre: this.addGenreForm.genre,
      };
      this.addGenre(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addGenreModal.hide();
      this.initForm();
    },
    removeGenre(genreID) {
      const path = `http://localhost:5000/genres/${genreID}/delete/`;
      axios.delete(path)
        .then((res) => {
          this.getGenres();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getGenres();
        });
    },
    onDeleteGenre(genre) {
      this.removeGenre(genre.id);
    },
  },
  created() {
    this.getGenres();
  },
};
</script>

<style scoped>
  .comp-style {
    padding: 15px;
    margin: 0 auto;
  }

  .table-width {
    max-width: 10cm;
    margin: 0 auto;
  }

  .btn-gr-ud {
    text-align: right;
    width: 55px;
  }
</style>
