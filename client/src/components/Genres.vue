<template>
  <b-container>
    <b-row>
      <first></first>
    </b-row>
    <b-row>
      <b-col col sm="7">
        <h1>Genres</h1>
        <hr>
        <br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.genre-modal>
          Add Genre
        </button>
        <br><br>
        <table class="table table-hover">
          <thead>
          <tr>
            <th scope="col">Genre</th>
            <th></th>
          </tr>
          </thead>
          <tbody v-for="(genre, index) in genres" :key="index">
          <tr>
            <td>{{ genre.genre }}</td>
            <td>
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
      </b-col>
    </b-row>
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
import First from './Navigation.vue';

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
    first: First,
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
