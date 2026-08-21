CREATE TABLE `equipment` (
	`id` text PRIMARY KEY NOT NULL,
	`asset_tag` text NOT NULL,
	`name` text NOT NULL,
	`category` text NOT NULL,
	`created_at` integer DEFAULT (cast(unixepoch('subsecond') * 1000 as integer)) NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX `equipment_asset_tag_unique` ON `equipment` (`asset_tag`);
--> statement-breakpoint
CREATE TABLE `loans` (
	`id` text PRIMARY KEY NOT NULL,
	`equipment_id` text NOT NULL,
	`responsible_name` text NOT NULL,
	`due_date` text NOT NULL,
	`loaned_at` integer DEFAULT (cast(unixepoch('subsecond') * 1000 as integer)) NOT NULL,
	`returned_at` integer,
	FOREIGN KEY (`equipment_id`) REFERENCES `equipment`(`id`) ON UPDATE no action ON DELETE restrict
);
--> statement-breakpoint
CREATE UNIQUE INDEX `one_active_loan_per_equipment` ON `loans` (`equipment_id`) WHERE `returned_at` IS NULL;
--> statement-breakpoint
INSERT INTO `equipment` (`id`, `asset_tag`, `name`, `category`) VALUES
  ('eq-projector-01', 'PROJ-001', 'Projetor multimídia', 'Audiovisual'),
  ('eq-notebook-01', 'NOTE-014', 'Notebook educacional', 'Informática'),
  ('eq-camera-01', 'CAM-003', 'Câmera fotográfica', 'Audiovisual'),
  ('eq-speaker-01', 'SOM-008', 'Caixa de som portátil', 'Áudio');
--> statement-breakpoint
INSERT INTO `loans` (`id`, `equipment_id`, `responsible_name`, `due_date`, `loaned_at`) VALUES
  ('loan-overdue-seed', 'eq-projector-01', 'Marina Lopes', date('now', '-2 day'), cast(unixepoch('subsecond', '-5 day') * 1000 as integer)),
  ('loan-active-seed', 'eq-notebook-01', 'João Ribeiro', date('now', '+3 day'), cast(unixepoch('subsecond', '-1 day') * 1000 as integer));
