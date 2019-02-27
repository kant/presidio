package recognizers

import (
	"context"
	"errors"
	"fmt"

	types "github.com/Microsoft/presidio-genproto/golang"

	store "github.com/Microsoft/presidio/presidio-api/cmd/presidio-api/api"
)

//InsertRecognizer Inserts a new custom pattern recognizer via the Recognizer
// store service
func InsertRecognizer(ctx context.Context,
	api *store.API,
	insertRecognizerRequest *types.RecognizerInsertOrUpdateRequest) (
	*types.RecognizersStoreResponse, error) {
	res, err := api.Services.InsertRecognizer(ctx,
		insertRecognizerRequest.Value)
	if err != nil {
		return nil, err
	}
	if res == nil {
		return nil, fmt.Errorf("No results")
	}
	return res, err
}

// UpdateRecognizer xxx
func UpdateRecognizer(ctx context.Context, rec *types.PatternRecognizer) (
	*types.RecognizersStoreResponse, error) {
	return nil, errors.New("Didnt implement yet")
}

// DeleteRecognizer xxx
func DeleteRecognizer(ctx context.Context, rec *types.PatternRecognizer) (
	*types.RecognizersStoreResponse, error) {
	return nil, errors.New("Didnt implement yet")
}

// GetRecognizer xxx
func GetRecognizer(ctx context.Context, name string) (
	*types.RecognizersGetResponse, error) {
	return nil, errors.New("Didnt implement yet")
}

// GetAllRecognizers xxx
func GetAllRecognizers(ctx context.Context) (
	*types.RecognizersGetResponse, error) {
	return nil, errors.New("Didnt implement yet")
}
