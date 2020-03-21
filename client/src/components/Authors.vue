<template>
  <b-container>
    <b-row><first></first></b-row>
    <b-row>
      <b-col col sm="10">
        <h1>Authors</h1>
        <hr>
        <br><br>
        <alert :dismiss=dismiss :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.author-modal>
          Add Author
        </button>
        <br><br>
        <table class="table table-hover">
          <thead>
          <tr>
            <th scope="col">Name</th>
            <th scope="col">Direction</th>
            <th scope="col">Date of Birth</th>
            <th></th>
          </tr>
          </thead>
          <tbody v-for="(author, index) in authors" :key="index">
          <tr>
            <td>{{ author.name }}</td>
            <td>{{ author.direction }}</td>
            <td>{{ author.date_of_birth }}</td>
            <td>
              <div class="btn-group" role="group">
                <button
                  type="button"
                  class="btn btn-warning btn-sm"
                  v-b-modal.author-update-modal
                  @click="editAuthor(author)">
                  Update
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="onDeleteAuthor(author)">
                  Delete
                </button>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
      </b-col>
    </b-row>
    <b-modal ref="addAuthorModal"
             id="author-modal"
             title="Add a new author"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-name-group"
                      label="Name:"
                      label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="addAuthorForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-direction-group"
                      label="Direction:"
                      label-for="form-direction-input">
          <b-form-input id="form-direction-input"
                        type="text"
                        v-model="addAuthorForm.direction"
                        required
                        placeholder="Enter direction">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-dob-group"
                      label="Date of birth:"
                      label-for="form-dob-input">
          <b-form-input id="form-dob-input"
                        type="text"
                        v-model="addAuthorForm.date_of_birth"
                        required
                        placeholder="Enter date of birth">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editAuthorModal"
             id="author-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-name-edit-group"
                      label="Name:"
                      label-for="form-name-edit-input">
          <b-form-input id="form-name-edit-input"
                        type="text"
                        v-model="editAuthorForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-direction-edit-group"
                      label="Direction:"
                      label-for="form-direction-edit-input">
          <b-form-input id="form-direction-edit-input"
                        type="text"
                        v-model="editAuthorForm.direction"
                        required
                        placeholder="Enter direction">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-dob-edit-group"
                      label="Date of birth:"
                      label-for="form-dob-edit-input">
          <b-form-input id="form-dob-edit-input"
                        type="text"
                        v-model="editAuthorForm.date_of_birth"
                        required
                        placeholder="Enter date of birth">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
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
        authors: [],
        addAuthorForm: {
          name: '',
          direction: '',
          date_of_birth: '',
        },
        editAuthorForm: {
          id: '',
        name: '',
        direction: '',
        date_of_birth: '',
      },
      message: '',
      dismiss: 0,
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
    first: First,
  },
  methods: {
    getAuthors() {
      const path = 'http://localhost:5000/authors/';
      axios.get(path)
        .then((res) => {
          this.authors = res.data.authors;
        })
        .catch((error) => {
          // eslint-отключение следующей строки
          console.error(error);
        });
    },
    addAuthor(payload) {
      const path = 'http://localhost:5000/authors/add/';
      axios.post(path, payload)
        .then((res) => {
          this.getAuthors();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-отключение следующей строки
          console.log(error);
          this.getAuthors();
        });
    },
    initForm() {
      this.addAuthorForm.name = '';
      this.addAuthorForm.direction = '';
      this.addAuthorForm.date_of_birth = '';
      this.editAuthorForm.name = '';
      this.editAuthorForm.direction = '';
      this.editAuthorForm.date_of_birth = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addAuthorModal.hide();
      const payload = {
        name: this.addAuthorForm.name,
        direction: this.addAuthorForm.direction,
        date_of_birth: this.addAuthorForm.date_of_birth,
      };
      this.addAuthor(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addAuthorModal.hide();
      this.initForm();
    },
    editAuthor(author) {
      this.editAuthorForm = author;
    },
    updateAuthor(payload, authorID) {
      const path = `http://localhost:5000/authors/${authorID}/edit/`;
      axios.put(path, payload)
        .then((res) => {
          this.getAuthors();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getAuthors();
        });
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editAuthorModal.hide();
      const payload = {
        name: this.editAuthorForm.name,
        direction: this.editAuthorForm.direction,
        date_of_birth: this.editAuthorForm.date_of_birth,
      };
      this.updateAuthor(payload, this.editAuthorForm.id);
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editAuthorModal.hide();
      this.initForm();
      this.getAuthors();
    },
    removeAuthor(authorID) {
      const path = `http://localhost:5000/authors/${authorID}/delete/`;
      axios.delete(path)
        .then((res) => {
          this.getAuthors();
          this.message = res.data.message;
          this.showMessage = true;
          alert.showAlert();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getAuthors();
        });
    },
    onDeleteAuthor(author) {
      this.removeAuthor(author.id);
    },
  },
  created() {
    this.getAuthors();
  },
};
</script>
