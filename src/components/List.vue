<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { p } from "../../../../../../opt/anaconda3/lib/python3.12/site-packages/bokeh/server/static/js/lib/core/dom";

const suites = ref([]);

onMounted(async () => {
  fetch("http://localhost:5000/train").then((response) => {
    console.log(response.ok ? "Training done" : "Training failed");
  });
  const response = await fetch("http://localhost:3000/suites");
  suites.value = await response.json();
});

const suiteToAdd = ref({
  nbRooms: 0,
  surface: 0,
  price: 0,
});

const predictions = ref({
  hasGarage: null,
  note: null,
});

const editingSuite = ref(null);

const saveToCsv = () => {
  fetch("http://localhost:3000/suites", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(suites.value),
  });
};

const addSuite = () => {
  suites.value.push({
    id: suites.value.length + 1,
    nbRooms: suiteToAdd.value.nbRooms,
    surface: suiteToAdd.value.surface,
    price: suiteToAdd.value.price,
  });
  resetSuiteToAdd();
  saveToCsv();
};

const resetSuiteToAdd = () => {
  suiteToAdd.value = {
    nbRooms: 1,
    surface: 5,
    price: 50000,
  };
};

const handleChange = () => {
  console.log("handleChange");
  // it should call the /predict/price endpoint when nbRooms and surface are set
  if (suiteToAdd.value.price && suiteToAdd.value.surface) {
    fetch(`http://localhost:5000/predict/garage`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        prix: suiteToAdd.value.price,
        surface: suiteToAdd.value.surface,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        predictions.value.hasGarage = data.garage;
      });
    fetch(`http://localhost:5000/predict/note`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        prix: suiteToAdd.value.price,
        surface: suiteToAdd.value.surface,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        predictions.value.note = data.note;
      });
  }
};

const startEditing = (suite) => {
  editingSuite.value = { ...suite };
};

const saveEdit = () => {
  const index = suites.value.findIndex((s) => s.id === editingSuite.value.id);
  if (index !== -1) {
    suites.value[index] = { ...editingSuite.value };
  }
  editingSuite.value = null;
  saveEdit();
};

const cancelEdit = () => {
  editingSuite.value = null;
};

const deleteSuite = (id) => {
  suites.value = suites.value.filter((s) => s.id !== id);
  saveToCsv();
};
</script>

<template>
  <h3>Liste d'appartements</h3>
  <div>
    <ul>
      <li v-for="suite in suites" :key="suite.id">
        <template v-if="editingSuite && editingSuite.id === suite.id">
          <input
            v-model="editingSuite.nbRooms"
            type="number"
            min="1"
            max="100"
          />
          <input
            v-model="editingSuite.surface"
            type="number"
            min="5"
            max="600"
          />
          <input
            v-model="editingSuite.price"
            type="number"
            min="50000"
            max="1000000"
          />
          <button @click="saveEdit">Enregistrer</button>
          <button @click="cancelEdit">Annuler</button>
        </template>
        <template v-else>
          <p>{{ suite.nbRooms }} pièces</p>
          <p>{{ suite.surface }} m²</p>
          <p>{{ suite.price }} €</p>
          <button @click="startEditing(suite)">Modifier</button>
          <button @click="deleteSuite(suite.id)">Supprimer</button>
        </template>
      </li>
    </ul>
    <form @submit.prevent="addSuite">
      <label for="nbRooms">Nombre de pièces</label>
      <input type="number" id="nbRooms" v-model="suiteToAdd.nbRooms" />
      <label for="surface">Surface</label>
      <input
        type="number"
        id="surface"
        v-model="suiteToAdd.surface"
        @change="handleChange"
      />
      <label for="price">Prix</label>
      <input
        type="number"
        id="price"
        v-model="suiteToAdd.price"
        @change="handleChange"
      />
      <div v-if="predictions.hasGarage !== null && predictions.note !== null">
        <h4>Predictions</h4>
        <p v-if="predictions.hasGarage">Il y a un garage</p>
        <p v-else>Il n'y a pas de garage</p>
        <p>La note estimée est de {{ predictions.note }}</p>
      </div>
      <button type="submit">Ajouter</button>
    </form>
  </div>
</template>

<style scoped>
div {
  margin-top: 1rem;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  border: 1px solid #ccc;
  padding: 1rem;
  margin: 1rem 0;
  max-width: 200px;
  p {
    width: max-content;
  }
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  position: fixed;
  right: 20px;
  top: 20px;
  height: 100vh;
  padding: 0 20px;
  border-left: 1px solid #ccc;
}

label {
  font-weight: bold;
}

input {
  padding: 0.5rem;
}

button {
  padding: 0.5rem;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  margin-right: 0.5rem;
}

button:last-child {
  margin-right: 0;
}
</style>
