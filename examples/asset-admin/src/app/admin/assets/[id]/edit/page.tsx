import { notFound } from "next/navigation";

import { updateAssetAction } from "@/app/admin/assets/actions";
import { AssetForm } from "@/components/asset-form";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { getAsset } from "@/features/assets/asset-data";

export default async function EditAssetPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const asset = await getAsset(id);
  if (!asset) notFound();
  const action = updateAssetAction.bind(null, id);

  return (
    <main className="mx-auto w-full max-w-3xl px-4 py-8 sm:px-6">
      <Card>
        <CardHeader>
          <CardTitle>Editar {asset.code}</CardTitle>
          <CardDescription>
            Atualize localização, responsável, situação ou demais dados do
            patrimônio.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <AssetForm action={action} asset={asset} />
        </CardContent>
      </Card>
    </main>
  );
}
