package main

import (
	"flag"
	"os"

	"github.com/spf13/pflag"
	"github.com/spf13/viper"

	"github.com/Microsoft/presidio/pkg/cache"
	log "github.com/Microsoft/presidio/pkg/logger"
	"github.com/Microsoft/presidio/pkg/platform"
	"github.com/Microsoft/presidio/pkg/platform/kube"
	"github.com/Microsoft/presidio/pkg/platform/local"
	"github.com/Microsoft/presidio/pkg/presidio/services"
	server "github.com/Microsoft/presidio/pkg/server"
)

func main() {

	pflag.Int(platform.WebPort, 8080, "HTTP listen port")
	pflag.String(platform.AnalyzerSvcAddress, "localhost:3000", "Analyzer service address")
	pflag.String(platform.AnonymizerSvcAddress, "localhost:3001", "Anonymizer service address")
	pflag.String(platform.SchedulerSvcAddress, "", "Scheduler service address")
	pflag.String(platform.RedisURL, "", "Redis address")
	pflag.String(platform.RedisPassword, "", "Redis db password (optional)")
	pflag.Int(platform.RedisDb, 0, "Redis db (optional)")
	pflag.Bool(platform.RedisSSL, false, "Redis ssl (optional)")
	pflag.String(platform.PresidioNamespace, "", "Presidio Kubernetes namespace (optional)")
	pflag.String("log_level", "info", "Log level - debug/info/warn/error")

	pflag.CommandLine.AddGoFlagSet(flag.CommandLine)
	pflag.Parse()
	viper.BindPFlags(pflag.CommandLine)

	settings := platform.GetSettings()
	log.CreateLogger(settings.LogLevel)

	svc := services.New(settings)

	var api *API

	// Setup Redis cache

	var cacheStore cache.Cache

	if settings.RedisURL != "" {
		cacheStore = svc.SetupCache()
	}

	// Kubernetes platform
	if settings.Namespace != "" {
		store, err := kube.New(settings.Namespace, "")
		if err != nil {
			log.Fatal(err.Error())
		}
		api = New(store, cacheStore, settings)
	} else {
		// Local platform
		store, err := local.New(os.TempDir())
		if err != nil {
			log.Fatal(err.Error())
		}
		api = New(store, cacheStore, settings)
	}

	api.setupGRPCServices()
	setupHTTPServer(api, settings.WebPort, settings.LogLevel)
}

func setupHTTPServer(api *API, port int, loglevel string) {

	r := server.Setup(port, loglevel)

	// api/v1 group
	v1 := r.Group("/api/v1")
	{
		// GET available field types
		v1.GET("fieldTypes", getFieldTypes)

		// templates group
		templates := v1.Group("/templates/:project")
		{
			// /api/v1/templates/123/analyze/1234
			// /api/v1/templates/123/anonymize/1234
			action := templates.Group("/:action")
			{
				// GET template
				action.GET(":id", api.getActionTemplate)
				// POST template
				action.POST(":id", api.postActionTemplate)
				// PUT, update template
				action.PUT(":id", api.putActionTemplate)
				// DELETE template
				action.DELETE(":id", api.deleteActionTemplate)
			}
		}

		// Actions group
		projects := v1.Group("projects/:project")
		{
			// Analyze text
			// /api/v1/projects/123/analyze
			projects.POST("/analyze", api.analyze)

			// Anonymize text
			// /api/v1/projects/123/anonymize
			projects.POST("/anonymize", api.anonymize)

			// Anonymize json
			// /api/v1/projects/123/anonymize-json
			projects.POST("/anonymize-json", api.anonymizeJSON)

			// Schedule scanning cron job
			// /api/v1/projects/123/schedule-scanner-cronjob
			projects.POST("/schedule-scanner-cronjob", api.scheduleScannerCronJob)

			// Schedule streams job
			// /api/v1/projects/123/schedule-streams-job
			projects.POST("/schedule-streams-job", api.scheduleStreamsJob)

		}

	}
	server.Start(r)
}
