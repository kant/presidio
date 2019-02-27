package main

import (
	"os"

	"github.com/stretchr/testify/assert"

	types "github.com/Microsoft/presidio-genproto/golang"
	"github.com/Microsoft/presidio/pkg/cache/mock"
	"github.com/Microsoft/presidio/pkg/platform"

	"testing"
)

func TestMain(m *testing.M) {
	os.Setenv("REDIS_URL", "fake_redis")
	settings = platform.GetSettings()
	os.Exit(m.Run())
}

// Insert and Get, verify it worked
func TestInsertAndGetRecognizer(t *testing.T) {
	// Mock the store with a fake redis
	recognizersStore = mock.New()

	// Insert a new pattern recognizer
	r := &types.RecognizerInsertOrUpdateRequest{}
	newRecognizer := types.PatternRecognizer{
		Name:     "DemoRecognizer1",
		Pattern:  "*FindMe*",
		Score:    0.123,
		Entity:   "DEMO_ITEMS",
		Language: "en"}
	r.Value = &newRecognizer
	_, err := applyInsertOrUpdate(r, false)
	assert.NoError(t, err)

	// Verify returned object is as expected
	getRequest := &types.RecognizerGetRequest{Name: newRecognizer.Name}
	getResponse, err := applyGet(getRequest)
	assert.NoError(t, err)
	assert.Equal(t, len(getResponse.Recognizers), 1)

	// Verify that the item is exactly as expected
	assert.Equal(t, &newRecognizer, getResponse.Recognizers[0])
}

// Try to update a non-existing item and expect to fail
func TestUpdateOfNonExisting(t *testing.T) {
	// Mock the store with a fake redis
	recognizersStore = mock.New()

	// Insert a new pattern recognizer
	r := &types.RecognizerInsertOrUpdateRequest{}
	// Update, expect to fail as this item does not exists
	_, err := applyInsertOrUpdate(r, true)
	assert.Error(t, err)
}

// Try to insert the same item again and expect to fail
func TestConflictingInserts(t *testing.T) {
	// Mock the store with a fake redis
	recognizersStore = mock.New()

	// Store is empty...
	rawValues, err := recognizersStore.Get(recognizersKey)
	assert.NoError(t, err)
	assert.Equal(t, rawValues, "")

	// Insert a new pattern recognizer
	r := &types.RecognizerInsertOrUpdateRequest{}
	newRecognizer1 := types.PatternRecognizer{
		Name:     "DemoRecognizer1",
		Pattern:  "*FindMe*",
		Score:    0.123,
		Entity:   "DEMO_ITEMS",
		Language: "en"}
	r.Value = &newRecognizer1
	_, err = applyInsertOrUpdate(r, false)
	assert.NoError(t, err)
	// This should fail
	_, err = applyInsertOrUpdate(r, false)
	assert.Error(t, err)

	// Verify just one item was returned
	getRequest := &types.RecognizersGetAllRequest{}
	getResponse, err := applyGetAll(getRequest)
	assert.NoError(t, err)
	assert.Equal(t, len(getResponse.Recognizers), 1)
}

// Try to insert several different items and expect to succeed
func TestMultipleDifferentInserts(t *testing.T) {
	// Mock the store with a fake redis
	recognizersStore = mock.New()

	// Store is empty...
	rawValues, err := recognizersStore.Get(recognizersKey)
	assert.NoError(t, err)
	assert.Equal(t, rawValues, "")

	// Insert a new pattern recognizer
	r := &types.RecognizerInsertOrUpdateRequest{}
	newRecognizer1 := types.PatternRecognizer{
		Name:     "DemoRecognizer1",
		Pattern:  "*FindMe*",
		Score:    0.123,
		Entity:   "DEMO_ITEMS",
		Language: "en"}
	r.Value = &newRecognizer1
	_, err = applyInsertOrUpdate(r, false)
	assert.NoError(t, err)

	r = &types.RecognizerInsertOrUpdateRequest{}
	newRecognizer2 := types.PatternRecognizer{
		Name:     "DemoRecognizer2",
		Pattern:  "*FindMeToo*",
		Score:    0.123,
		Entity:   "DEMO_ITEMS",
		Language: "en"}
	r.Value = &newRecognizer2
	_, err = applyInsertOrUpdate(r, false)
	assert.NoError(t, err)

	// Verify returned object is as expected
	getRequest := &types.RecognizersGetAllRequest{}
	getResponse, err := applyGetAll(getRequest)
	assert.NoError(t, err)
	assert.Equal(t, len(getResponse.Recognizers), 2)
}

// Delete the only existing item and expect to succeed
func TestDeleteOnlyRecognizer(t *testing.T) {
	// Mock the store with a fake redis
	recognizersStore = mock.New()

	// Store is empty...
	rawValues, err := recognizersStore.Get(recognizersKey)
	assert.NoError(t, err)
	assert.Equal(t, rawValues, "")

	// Insert a new pattern recognizer
	r := &types.RecognizerInsertOrUpdateRequest{}
	deletedRecognizer := types.PatternRecognizer{
		Name:     "DemoRecognizer1",
		Pattern:  "*FindMe*",
		Score:    0.123,
		Entity:   "DEMO_ITENS",
		Language: "en"}
	r.Value = &deletedRecognizer
	_, err = applyInsertOrUpdate(r, false)
	assert.NoError(t, err)

	// Delete
	deleteRequest := &types.RecognizerDeleteRequest{Name: deletedRecognizer.Name}
	_, err = applyDelete(deleteRequest)
	assert.NoError(t, err)

	// Get should fail as it was already deleted
	getRequest := &types.RecognizerGetRequest{Name: deletedRecognizer.Name}
	_, err = applyGet(getRequest)
	assert.Error(t, err)
}

func TestDeleteRecognizer(t *testing.T) {
	// Mock the store with a fake redis
	recognizersStore = mock.New()

	// Store is empty...
	rawValues, err := recognizersStore.Get(recognizersKey)
	assert.NoError(t, err)
	assert.Equal(t, rawValues, "")

	// Insert a new pattern recognizer
	r := &types.RecognizerInsertOrUpdateRequest{}
	insertRecognizer := types.PatternRecognizer{
		Name:     "DemoRecognizer1",
		Pattern:  "*FindMe*",
		Score:    0.123,
		Entity:   "DEMO_ITEMS",
		Language: "en"}
	r.Value = &insertRecognizer
	_, err = applyInsertOrUpdate(r, false)
	assert.NoError(t, err)

	// Insert a second item
	insertRecognizer = types.PatternRecognizer{
		Name:     "DemoRecognizer2",
		Pattern:  "*FindMeToo*",
		Score:    0.123,
		Entity:   "DEMO_ITEMS",
		Language: "en"}
	r.Value = &insertRecognizer
	_, err = applyInsertOrUpdate(r, false)
	assert.NoError(t, err)

	// Get should succeed with 2 values
	getRequest := &types.RecognizersGetAllRequest{}
	getResponse, err := applyGetAll(getRequest)
	assert.NoError(t, err)
	assert.Equal(t, len(getResponse.Recognizers), 2)

	// Delete
	deleteRequest := &types.RecognizerDeleteRequest{Name: "DemoRecognizer1"}
	_, err = applyDelete(deleteRequest)
	assert.NoError(t, err)

	// Get should succeed with just 1 value
	getRequest = &types.RecognizersGetAllRequest{}
	getResponse, err = applyGetAll(getRequest)
	assert.NoError(t, err)
	assert.Equal(t, len(getResponse.Recognizers), 1)
}

// Try to delete a non-existing item and expect to fail
func TestDeleteNonExistingRecognizer(t *testing.T) {
	// Mock the store with a fake redis
	recognizersStore = mock.New()

	// Store is empty...
	rawValues, err := recognizersStore.Get(recognizersKey)
	assert.NoError(t, err)
	assert.Equal(t, rawValues, "")

	// Delete
	deleteRequest := &types.RecognizerDeleteRequest{Name: "someName"}
	_, err = applyDelete(deleteRequest)
	assert.Error(t, err)
}
