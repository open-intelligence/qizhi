package db

import (
	"fmt"

	"github.com/spf13/cobra"

	"ModelHub-server/models"
)

var createIndexesFlags struct {
	cluster string
	db      string
	coll    string
	pos     int
}

func init() {
	CreateIndexesCmd.Flags().StringVar(&createIndexesFlags.cluster, "cluster", "hub", "which cluster")
	CreateIndexesCmd.Flags().StringVar(&createIndexesFlags.db, "db", "hub", "which db")
	CreateIndexesCmd.Flags().StringVar(&createIndexesFlags.coll, "coll", "", "which collection, empty means all collections in db")
	CreateIndexesCmd.Flags().IntVar(&createIndexesFlags.pos, "pos", -1, "which index, postion in index array, -1 means all")
}

var CreateIndexesCmd = &cobra.Command{
	Use:   "createIndexes",
	Short: "Create indexes",
	Long:  `Create indexes.`,
	RunE: func(cmd *cobra.Command, args []string) error {
		err := models.CreateDBIndexes(createIndexesFlags.cluster, createIndexesFlags.db, createIndexesFlags.coll, createIndexesFlags.pos)
		if err != nil {
			return err
		}

		fmt.Println("create indexes ok")
		return nil
	},
}
