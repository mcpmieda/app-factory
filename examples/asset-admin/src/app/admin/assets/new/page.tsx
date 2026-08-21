import { createAssetAction } from "@/app/admin/assets/actions";
import { AssetForm } from "@/components/asset-form";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function NewAssetPage() {
  return (
    <main className="mx-auto w-full max-w-3xl px-4 py-8 sm:px-6">
      <Card>
        <CardHeader>
          <CardTitle>Novo patrimônio</CardTitle>
          <CardDescription>
            Cadastre somente dados fictícios nesta aplicação de validação.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <AssetForm action={createAssetAction} />
        </CardContent>
      </Card>
    </main>
  );
}
