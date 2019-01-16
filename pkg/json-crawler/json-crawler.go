package jsoncrawler

import (
	"container/list"
	"context"
	"fmt"
	"regexp"

	types "github.com/Microsoft/presidio-genproto/golang"
	"github.com/oliveagle/jsonpath"
)

type analyzeFunc func(ctx context.Context, text string, template *types.AnalyzeTemplate) ([]*types.AnalyzeResult, error)
type anonymizeFunc func(ctx context.Context, analyzeResults []*types.AnalyzeResult, text string, anonymizeTemplate *types.AnonymizeTemplate) (*types.AnonymizeResponse, error)

const fieldNameRegex = "<[A-Z]+(_*[A-Z]*)*>"

//JSONCrawler for analyzing and anonymizing text
type JSONCrawler struct {
	analyzeItem       analyzeFunc
	anonymizeItem     anonymizeFunc
	ctx               context.Context
	analyzeTemplate   *types.AnalyzeTemplate
	anonymizeTemplate *types.AnonymizeTemplate
}

//New JSONCrawler
func New(ctx context.Context, analyze analyzeFunc, anonymize anonymizeFunc, analyzeTemplate *types.AnalyzeTemplate, anonymizeTemplate *types.AnonymizeTemplate) *JSONCrawler {
	return &JSONCrawler{
		analyzeItem:       analyze,
		anonymizeItem:     anonymize,
		ctx:               ctx,
		analyzeTemplate:   analyzeTemplate,
		anonymizeTemplate: anonymizeTemplate,
	}
}

func (jsonCrawler *JSONCrawler) ReplaceValue(path string, json interface{}) (interface{}, error) {
	res, err := jsonpath.JsonPathLookup(json, path)
}

// ScanJSON scan the json in DFS to get to all the nodes
func (jsonCrawler *JSONCrawler) ScanJSON(valuesMap map[string]interface{}) error {
	err := checkIfEmptyMap(valuesMap)
	if err != nil {
		return err
	}

	queue := list.New()

	queue.PushFront(valuesMap)

	for queue.Len() > 0 {
		current := queue.Front()
		queue.Remove(current)

		currentValue := current.Value.(map[string]interface{})
		for key, val := range currentValue {
			switch concreteVal := val.(type) {
			case map[string]interface{}:
				for _, val := range concreteVal {
					queue.PushFront(val)
				}

			case []interface{}:
				for i, arrayval := range concreteVal {
					switch concreteArrayVal := arrayval.(type) {
					case map[string]interface{}:
						queue.PushFront(arrayval)
					default:
						anonymizedVal, err := jsonCrawler.analyzeAndAnonymizeJSON(fmt.Sprint(concreteArrayVal))
						if err != nil {
							return err
						}
						concreteVal[i] = anonymizedVal
					}
				}
			default:
				anonymizedVal, err := jsonCrawler.analyzeAndAnonymizeJSON(fmt.Sprint(concreteVal))
				if err != nil {
					return err
				}
				currentValue[key] = anonymizedVal
			}
		}

	}

	return nil
}

// func (jsonCrawler *JSONCrawler) scanArray(schemaArray []interface{}, valuesArray []interface{}) error {
// 	err := checkIfEmptyArray(schemaArray, valuesArray)
// 	if err != nil {
// 		return err
// 	}

// 	i := 0
// 	for j := range valuesArray {
// 		if len(schemaArray) > 1 {
// 			i = j
// 		}

// 		val := schemaArray[i]
// 		switch concreteVal := val.(type) {
// 		case map[string]interface{}:
// 			err := jsonCrawler.ScanJSON(val.(map[string]interface{}), valuesArray[j].(map[string]interface{}))
// 			if err != nil {
// 				return err
// 			}
// 		case []interface{}:
// 			err := jsonCrawler.scanArray(val.([]interface{}), valuesArray[j].([]interface{}))
// 			if err != nil {
// 				return err
// 			}
// 		default:
// 			newVal, err := jsonCrawler.analyzeAndAnonymizeJSON(fmt.Sprint(valuesArray[j]), fmt.Sprint(concreteVal))
// 			if err != nil {
// 				return err
// 			}
// 			valuesArray[j] = newVal
// 		}
// 	}

// 	return nil
// }

// func (jsonCrawler *JSONCrawler) scanIfNotEmpty(valuesMap map[string]interface{}, key string, val interface{}, valType string) error {
// 	newVal, err := checkIfKeyExistInMap(valuesMap, key)
// 	if err != nil {
// 		return err
// 	}
// 	if valType == "map" {
// 		return jsonCrawler.ScanJSON(val.(map[string]interface{}), newVal.(map[string]interface{}))
// 	}

// 	return jsonCrawler.scanArray(val.([]interface{}), newVal.([]interface{}))
// }

func (jsonCrawler *JSONCrawler) analyzeAndAnonymizeJSON(val string) (string, error) {
	match, err := regexp.MatchString(fieldNameRegex, val)
	if err != nil {
		return "", err
	}

	if match {
		return val, nil
	}

	analyzeResults, err := jsonCrawler.analyzeItem(jsonCrawler.ctx, val, jsonCrawler.analyzeTemplate)
	if err != nil {
		return "", err
	}
	return jsonCrawler.getAnonymizeResult(val, analyzeResults)
}

func (jsonCrawler *JSONCrawler) getAnonymizeResult(text string, analyzeResults []*types.AnalyzeResult) (string, error) {
	result, err := jsonCrawler.anonymizeItem(jsonCrawler.ctx, analyzeResults, text, jsonCrawler.anonymizeTemplate)
	if err != nil {
		return "", err
	}
	return result.Text, nil
}

func checkIfKeyExistInMap(valuesMap map[string]interface{}, key string) (interface{}, error) {
	if newVal, ok := valuesMap[key]; ok {
		return newVal, nil
	}
	return nil, fmt.Errorf("errorMsg")
}

func checkIfEmptyMap(json map[string]interface{}) error {
	if json == nil || len(json) == 0 {
		return fmt.Errorf("Json is empty")
	}
	return nil
}

func checkIfEmptyArray(json []interface{}) error {
	if json == nil || len(json) == 0 {
		return fmt.Errorf("errorMsg")
	}
	return nil
}

func buildAnalyzeResult(text string, field string) []*types.AnalyzeResult {
	return [](*types.AnalyzeResult){
		&types.AnalyzeResult{
			Text: text,
			Field: &types.FieldTypes{
				Name: field,
			},
			Score: 1,
			Location: &types.Location{
				Start: 0,
				End:   int32(len(text)),
			},
		},
	}
}
