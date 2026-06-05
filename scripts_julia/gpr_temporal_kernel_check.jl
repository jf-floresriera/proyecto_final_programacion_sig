# Verificación numérica del kernel RBF temporal usado conceptualmente en el gap-filling GPR.
# Este script no reemplaza el flujo GEE; sirve como comprobación independiente en Julia.

using LinearAlgebra
using Statistics

function rbf_kernel(t1::AbstractVector, t2::AbstractVector; ell::Float64=30.0, sigma_f::Float64=1.0)
    K = Matrix{Float64}(undef, length(t1), length(t2))
    for i in eachindex(t1), j in eachindex(t2)
        K[i, j] = sigma_f^2 * exp(-0.5 * ((t1[i] - t2[j])^2) / ell^2)
    end
    return K
end

function gpr_predict(t_train, y_train, t_star; ell=30.0, sigma_f=1.0, sigma_n=0.05)
    K = rbf_kernel(t_train, t_train; ell=ell, sigma_f=sigma_f) .+ (sigma_n^2) .* I
    Ks = rbf_kernel(t_train, t_star; ell=ell, sigma_f=sigma_f)
    alpha = cholesky(Symmetric(K)) \ y_train
    return transpose(Ks) * alpha
end

# Ejemplo mínimo reproducible con una serie fenológica sintética.
t_train = [100.0, 120.0, 150.0, 180.0, 210.0, 240.0]
y_train = [0.3, 0.8, 1.9, 2.8, 1.7, 0.6]
t_star = collect(100.0:10.0:240.0)
y_hat = gpr_predict(t_train, y_train, t_star; ell=30.0, sigma_f=1.0, sigma_n=0.05)

println("Predicción GPR temporal en Julia")
println(hcat(t_star, y_hat))
