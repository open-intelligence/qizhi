package cmd

import (
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
	"fmt"
	"os"
	"github.com/fsnotify/fsnotify"
	log "github.com/sirupsen/logrus"
	"path/filepath"
)

var rootFlags struct {
	cfgFile string
}

var rootCmd = &cobra.Command{
	Use:"hub",
	Short:"deep learning model hub server",
	Long:"deep learning model hub server by pkuml",
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}

func initConfig() {
	if e := os.Getenv("MODEL_HUB_CONFIG_FILE"); e != "" {
		rootFlags.cfgFile = e
	}
	viper.SetConfigFile(rootFlags.cfgFile)
	err := viper.ReadInConfig()
	if err != nil {
		panic(err)
	}
	fmt.Println("using config file: ", viper.ConfigFileUsed())

	viper.WatchConfig()
	viper.OnConfigChange(func(e fsnotify.Event) {
		fmt.Println("config changed")
	})
}

func initLog() {
	log.SetFormatter(&log.JSONFormatter{})


	level, err := log.ParseLevel(viper.GetString("log.level"))
	if err != nil {
		panic(err)
	}
	log.SetLevel(level)

	w, err := os.OpenFile(filepath.Join(viper.GetString("dir.data"), viper.GetString("log.app.file")), os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0640)
	if err != nil {
		panic(err)
	}
	log.SetOutput(w)
}

func init() {
	cobra.OnInitialize(initConfig, initLog)

	rootCmd.PersistentFlags().StringVarP(&rootFlags.cfgFile, "config", "c", "./config.json", "config file")
	rootCmd.PersistentFlags().String("env", "", "environment")
	rootCmd.PersistentFlags().String("dir.data", "", "directory for data")
	rootCmd.PersistentFlags().String("log.level", "", "log filter level")

	viper.BindPFlags(rootCmd.PersistentFlags())

	rootCmd.AddCommand()
}